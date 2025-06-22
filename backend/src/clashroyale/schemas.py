from typing import Dict, List, Optional
from pydantic import BaseModel, RootModel


class IconUrls(BaseModel):
    medium: str
    evolutionMedium: Optional[str] = None


class Card(BaseModel):
    name: str
    id: int
    level: int
    maxLevel: int
    maxEvolutionLevel: Optional[int] = None
    evolutionLevel: Optional[int] = None
    starLevel: Optional[int] = None
    rarity: str
    count: int
    elixirCost: int
    iconUrls: IconUrls


class Arena(BaseModel):
    id: int
    name: str


class Clan(BaseModel):
    tag: str
    name: str
    badgeId: int


class PathOfLegendSeasonResult(BaseModel):
    leagueNumber: int
    trophies: int
    rank: Optional[int] = None


class ArenaProgress(BaseModel):
    arena: Arena
    trophies: int
    bestTrophies: int


class Progress(RootModel[Dict[str, ArenaProgress]]):
    def __getitem__(self, key: str):
        return self.__root__.get(key)

    def __iter__(self):
        return iter(self.__root__.items())


class SeasonStats(BaseModel):
    id: Optional[str] = None
    trophies: int


class LeagueStatistics(BaseModel):
    currentSeason: Dict[str, int]
    previousSeason: SeasonStats
    bestSeason: SeasonStats


class Badge(BaseModel):
    name: str
    level: int
    maxLevel: int
    progress: int
    target: int
    iconUrls: Dict[str, str]


class Achievement(BaseModel):
    name: str
    stars: int
    value: int
    target: int
    info: str
    completionInfo: Optional[str] = None


class Player(BaseModel):
    tag: str
    name: str
    expLevel: int
    trophies: int
    bestTrophies: int
    wins: int
    losses: int
    battleCount: int
    threeCrownWins: int
    challengeCardsWon: int
    challengeMaxWins: int
    tournamentCardsWon: int
    tournamentBattleCount: int
    role: str
    donations: int
    donationsReceived: int
    totalDonations: int
    warDayWins: int
    clanCardsCollected: int
    clan: Clan
    arena: Arena
    leagueStatistics: LeagueStatistics
    badges: List[Badge]
    achievements: List[Achievement]
    cards: List[Card]
    currentDeck: List[Card]
    currentDeckSupportCards: List[Card]
    currentFavouriteCard: Card
    starPoints: int
    expPoints: int
    legacyTrophyRoadHighScore: int
    currentPathOfLegendSeasonResult: PathOfLegendSeasonResult
    lastPathOfLegendSeasonResult: PathOfLegendSeasonResult
    bestPathOfLegendSeasonResult: PathOfLegendSeasonResult
    progress: Progress
    totalExpPoints: int
    supportCards: List[Card]

    class Config:
        populate_by_name = True
