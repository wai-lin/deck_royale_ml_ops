from typing import Dict, List, Optional
from pydantic import BaseModel, RootModel


class IconUrls(BaseModel):
    medium: Optional[str] = None
    evolutionMedium: Optional[str] = None


class Card(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    level: Optional[int] = None
    maxLevel: Optional[int] = None
    maxEvolutionLevel: Optional[int] = None
    evolutionLevel: Optional[int] = None
    starLevel: Optional[int] = None
    rarity: Optional[str] = None
    count: Optional[int] = None
    elixirCost: Optional[int] = None
    iconUrls: Optional[IconUrls] = None


class Arena(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Clan(BaseModel):
    tag: Optional[str] = None
    name: Optional[str] = None
    badgeId: Optional[int] = None


class PathOfLegendSeasonResult(BaseModel):
    leagueNumber: Optional[int] = None
    trophies: Optional[int] = None
    rank: Optional[int] = None


class ArenaProgress(BaseModel):
    arena: Optional[Arena] = None
    trophies: Optional[int] = None
    bestTrophies: Optional[int] = None


class Progress(RootModel[Dict[str, ArenaProgress]]):
    def __getitem__(self, key: str):
        return self.__root__.get(key)

    def __iter__(self):
        return iter(self.__root__.items())


class SeasonStats(BaseModel):
    id: Optional[str] = None
    trophies: Optional[int] = None


class LeagueStatistics(BaseModel):
    currentSeason: Optional[Dict[str, int]] = None
    previousSeason: Optional[SeasonStats] = None
    bestSeason: Optional[SeasonStats] = None


class Badge(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    maxLevel: Optional[int] = None
    progress: Optional[int] = None
    target: Optional[int] = None
    iconUrls: Optional[Dict[str, str]] = None


class Achievement(BaseModel):
    name: Optional[str] = None
    stars: Optional[int] = None
    value: Optional[int] = None
    target: Optional[int] = None
    info: Optional[str] = None
    completionInfo: Optional[str] = None


class Player(BaseModel):
    tag: Optional[str] = None
    name: Optional[str] = None
    expLevel: Optional[int] = None
    trophies: Optional[int] = None
    bestTrophies: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    battleCount: Optional[int] = None
    threeCrownWins: Optional[int] = None
    challengeCardsWon: Optional[int] = None
    challengeMaxWins: Optional[int] = None
    tournamentCardsWon: Optional[int] = None
    tournamentBattleCount: Optional[int] = None
    role: Optional[str] = None
    donations: Optional[int] = None
    donationsReceived: Optional[int] = None
    totalDonations: Optional[int] = None
    warDayWins: Optional[int] = None
    clanCardsCollected: Optional[int] = None
    clan: Optional[Clan] = None
    arena: Optional[Arena] = None
    leagueStatistics: Optional[LeagueStatistics] = None
    badges: Optional[List[Badge]] = None
    achievements: Optional[List[Achievement]] = None
    cards: Optional[List[Card]] = None
    currentDeck: Optional[List[Card]] = None
    currentDeckSupportCards: Optional[List[Card]] = None
    currentFavouriteCard: Optional[Card] = None
    starPoints: Optional[int] = None
    expPoints: Optional[int] = None
    legacyTrophyRoadHighScore: Optional[int] = None
    currentPathOfLegendSeasonResult: Optional[PathOfLegendSeasonResult] = None
    lastPathOfLegendSeasonResult: Optional[PathOfLegendSeasonResult] = None
    bestPathOfLegendSeasonResult: Optional[PathOfLegendSeasonResult] = None
    progress: Optional[Progress] = None
    totalExpPoints: Optional[int] = None
    supportCards: Optional[List[Card]] = None

    class Config:
        populate_by_name = True
