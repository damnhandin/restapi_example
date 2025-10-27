from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    @property
    def database_url(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port,
        )


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).
    """

    other_params: str = None

    @staticmethod
    def from_env(env: Env):
        return Miscellaneous(other_params=None)


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    """

    db: DbConfig
    misc: Miscellaneous


def load_config(env: Env | None = None, path: str | None = None) -> Config:
    # Create an Env object.
    # The Env object will be used to read environment variables.
    if not env:
        env = Env()
        env.read_env(path)

    return Config(
        db=DbConfig.from_env(env),
        misc=Miscellaneous.from_env(env),
    )
