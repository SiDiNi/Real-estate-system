"""add_payment_triggers_and_logs

Revision ID: 111sql111
Revises:
Create Date: 2026-05-15 ...

"""

import sqlalchemy as sa

from alembic import op


revision = "111sql111"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ==========================================
    # 1. Таблица для логов
    # ==========================================
    op.execute("""
        CREATE TABLE IF NOT EXISTS payment_logs (
            id SERIAL PRIMARY KEY,
            payment_id INTEGER,
            amount NUMERIC(10, 2),
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message TEXT
        );
    """)

    # ==========================================
    # ТРИГГЕР 1: Автоматическое снятие объекта с продажи при аренде
    # ==========================================

    # 1.1 Создаём функцию
    op.execute("""
        CREATE OR REPLACE FUNCTION update_property_status_on_contract()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (TG_OP = 'INSERT') THEN
                UPDATE properties
                SET is_available = false
                WHERE id = NEW.property_id;
            ELSIF (TG_OP = 'DELETE' OR (TG_OP = 'UPDATE' AND NEW.status = 'completed')) THEN
                UPDATE properties
                SET is_available = true
                WHERE id = OLD.property_id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # 1.2 Создаём триггер (отдельно!)
    op.execute("""
        DROP TRIGGER IF EXISTS trg_contract_property_status ON contracts;
    """)

    op.execute("""
        CREATE TRIGGER trg_contract_property_status
            AFTER INSERT OR UPDATE OR DELETE ON contracts
            FOR EACH ROW
            EXECUTE FUNCTION update_property_status_on_contract();
    """)

    # ==========================================
    # ТРИГГЕР 2: Логирование всех платежей (Аудит)
    # ==========================================

    # 2.1 Функция
    op.execute("""
        CREATE OR REPLACE FUNCTION log_payment_creation()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO payment_logs (payment_id, amount, message)
            VALUES (NEW.id, NEW.amount, 'Создан новый платеж');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # 2.2 Триггер
    op.execute("""
        DROP TRIGGER IF EXISTS trg_log_payment ON payments;
    """)

    op.execute("""
        CREATE TRIGGER trg_log_payment
            AFTER INSERT ON payments
            FOR EACH ROW
            EXECUTE FUNCTION log_payment_creation();
    """)

    # ==========================================
    # ТРИГГЕР 3: Запрет отрицательных сумм платежей
    # ==========================================

    # 3.1 Функция
    op.execute("""
        CREATE OR REPLACE FUNCTION check_positive_amount()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (NEW.amount < 0) THEN
                RAISE EXCEPTION 'Нельзя внести платеж с отрицательной суммой! Попробуйте положительное число.';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # 3.2 Триггер
    op.execute("""
        DROP TRIGGER IF EXISTS trg_check_payment_amount ON payments;
    """)

    op.execute("""
        CREATE TRIGGER trg_check_payment_amount
            BEFORE INSERT OR UPDATE ON payments
            FOR EACH ROW
            EXECUTE FUNCTION check_positive_amount();
    """)


def downgrade() -> None:
    # Удаляем в обратном порядке
    op.execute("DROP TRIGGER IF EXISTS trg_contract_property_status ON contracts;")
    op.execute("DROP FUNCTION IF EXISTS update_property_status_on_contract();")

    op.execute("DROP TRIGGER IF EXISTS trg_log_payment ON payments;")
    op.execute("DROP FUNCTION IF EXISTS log_payment_creation();")

    op.execute("DROP TRIGGER IF EXISTS trg_check_payment_amount ON payments;")
    op.execute("DROP FUNCTION IF EXISTS check_positive_amount();")

    op.execute("DROP TABLE IF EXISTS payment_logs;")
