"use client";
import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import PlayerStint from "../../../components/PlayerStint";

interface Player {
  id: number;
  name: string;
  position: string;
}

interface Stint {
  period: number;
  startTime: string;
  endTime: string;
}

interface Lineup {
  game_id: number;
  team_id: number;
  lineup_num: number;
  period: number;
  time_in: string;
  time_out: string;
  [key: string]: number | string | null;
}

const GameStintsPage: React.FC = () => {
  const params = useParams();
  const teamId = process.env.NEXT_PUBLIC_TEAM_ID;
  const gameId = params.gameid;
  const [players, setPlayers] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [stints, setStints] = useState<Stint[]>([]);
  const [playersCache, setPlayersCache] = useState<Map<string, Player[]>>(
    new Map()
  );
  const [stintsCache, setStintsCache] = useState<Map<string, Stint[]>>(
    new Map()
  );

  const fetchPlayers = useCallback(
    async (gameId: string, teamId: string) => {
      const cacheKey = `${gameId}-${teamId}`;
      if (playersCache.has(cacheKey)) {
        setPlayers(playersCache.get(cacheKey)!);
        return;
      }

      try {
        const response = await fetch(
          `/api/lineups/wide?game_id=${gameId}&team_id=${teamId}`,
          {
            credentials: "include",
          }
        );
        const data: { lineups: Lineup[] } = await response.json();
        const uniquePlayers = new Map<number, Player>();
        data.lineups.forEach((lineup: Lineup) => {
          for (let i = 1; i <= 5; i++) {
            const playerId = lineup[`player${i}_id`];
            const playerName = lineup[`player${i}_name`];
            const playerPosition = lineup[`player${i}_position`];
            if (playerId && playerName && playerPosition) {
              if (!uniquePlayers.has(Number(playerId))) {
                uniquePlayers.set(Number(playerId), {
                  id: Number(playerId),
                  name: String(playerName),
                  position: String(playerPosition),
                });
              }
            }
          }
        });
        const playersList = Array.from(uniquePlayers.values());
        setPlayers(playersList);
        setPlayersCache(new Map(playersCache.set(cacheKey, playersList)));
      } catch (error) {
        console.error("Error fetching players:", error);
      }
    },
    [playersCache]
  );

  const fetchPlayerStints = useCallback(
    async (gameId: string, teamId: string, playerId: number) => {
      const cacheKey = `${gameId}-${teamId}-${playerId}`;
      if (stintsCache.has(cacheKey)) {
        setStints(stintsCache.get(cacheKey)!);
        return;
      }

      try {
        const response = await fetch(
          `/api/lineups/wide?game_id=${gameId}&team_id=${teamId}&player_id=${playerId}`
        );
        const data: { lineups: Lineup[] } = await response.json();
        const playerStints = data.lineups.map((lineup) => ({
          period: Number(lineup.period),
          startTime: String(lineup.time_in),
          endTime: String(lineup.time_out),
        }));
        setStints(playerStints);
        setStintsCache(new Map(stintsCache.set(cacheKey, playerStints)));
      } catch (error) {
        console.error("Error fetching player stints:", error);
      }
    },
    [stintsCache]
  );

  useEffect(() => {
    if (gameId && teamId) {
      fetchPlayers(String(gameId), String(teamId));
    }
  }, [gameId, teamId, fetchPlayers]);

  useEffect(() => {
    if (selectedPlayer && gameId && teamId) {
      fetchPlayerStints(String(gameId), String(teamId), selectedPlayer.id);
    }
  }, [selectedPlayer, gameId, teamId, fetchPlayerStints]);

  // Add this useEffect to log the stints data
  useEffect(() => {
    if (stints.length > 0) {
      console.log("Player stints:", stints);
    }
  }, [stints]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Game Stints</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="col-span-1">
          <h2 className="text-xl font-semibold mb-2">Players</h2>
          <ul className="bg-white shadow-md rounded-lg overflow-hidden text-gray-800">
            {players.map((player) => (
              <li
                key={player.id}
                className={`p-2 cursor-pointer hover:bg-gray-100 ${
                  selectedPlayer?.id === player.id ? "bg-blue-100" : ""
                }`}
                onClick={() => setSelectedPlayer(player)}
              >
                {player.name} ({player.position})
              </li>
            ))}
          </ul>
        </div>
        <div className="col-span-2">
          <h2 className="text-xl font-semibold mb-2">Player Stints</h2>
          {selectedPlayer && stints.length > 0 && (
            <PlayerStint
              playerName={selectedPlayer.name}
              playerPosition={selectedPlayer.position}
              stints={stints}
            />
          )}
          {selectedPlayer && stints.length === 0 && (
            <p>No stints data available for this player.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default GameStintsPage;
