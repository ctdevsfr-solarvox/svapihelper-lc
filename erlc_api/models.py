from dataclasses import dataclass


@dataclass
class Player:
    id: int
    username: str
    team: str
    rank: str

    @staticmethod
    def from_dict(d: dict):
        return Player(
            id=d.get("id"),
            username=d.get("username"),
            team=d.get("team"),
            rank=d.get("rank")
        )


@dataclass
class ServerInfo:
    player_count: int
    max_players: int
    queue: int

    @staticmethod
    def from_dict(d: dict):
        return ServerInfo(
            player_count=d.get("playerCount"),
            max_players=d.get("maxPlayers"),
            queue=d.get("queue")
        )


@dataclass
class Call:
    caller: str
    location: str
    type: str

    @staticmethod
    def from_dict(d: dict):
        return Call(
            caller=d.get("caller"),
            location=d.get("location"),
            type=d.get("type")
        )
