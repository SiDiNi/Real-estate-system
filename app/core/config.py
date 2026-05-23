from dataclasses import dataclass

from environs import Env


@dataclass
class API:
    secret_key: str
    algorithm: str
    live_time_token: int
    host: str
    port: str


@dataclass
class DataBase:
    host: str
    port: str
    name: str
    user: str
    password: str

    name_test: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def database_test(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name_test}"


@dataclass
class Config:
    api: API
    db: DataBase


def load_config(data: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(data)

    return Config(
        api=API(
            secret_key=env("SECRET_KEY"),
            algorithm=env("ALGORITHM"),
            live_time_token=env.int("LIVE_TIME_TOKEN_MINUTES"),
            host=env("API_HOST"),
            port=env("API_PORT"),
        ),
        db=DataBase(
            host=env("DB_HOST"),
            port=env("DB_PORT"),
            name=env("DB_NAME"),
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
            name_test=env("DB_NAME_TEST"),
        ),
    )


config = load_config()
