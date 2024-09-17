'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import PlayerStint from '../../components/PlayerStint';

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
  const searchParams = useSearchParams();
  const gameId = searchParams.get('game_id');

  const [players, setPlayers] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [stints, setStints] = useState<Stint[]>([]);

  useEffect(() => {
    if (gameId) {
      fetchPlayers(gameId);
    }
  }, [gameId]);

  useEffect(() => {
    if (selectedPlayer && gameId) {
      fetchPlayerStints(gameId, selectedPlayer.id);
    }
  }, [selectedPlayer, gameId]);

  const fetchPlayers = async (gameId: string) => {
    try {
      const response = await fetch(`/api/lineups/wide?game_id=${gameId}`);
      const data: { lineups: Lineup[] } = await response.json();
      const uniquePlayers = new Set<Player>();
      data.lineups.forEach((lineup: Lineup) => {
        for (let i = 1; i <= 5; i++) {
          const playerId = lineup[`player${i}_id`];
          const playerName = lineup[`player${i}_name`];
          const playerPosition = lineup[`player${i}_position`];
          if (playerId && playerName && playerPosition) {
            uniquePlayers.add({
              id: Number(playerId),
              name: String(playerName),
              position: String(playerPosition),
            });
          }
        }
      });
      setPlayers(Array.from(uniquePlayers));
    } catch (error) {
      console.error('Error fetching players:', error);
    }
  };

  const fetchPlayerStints = async (gameId: string, playerId: number) => {
    try {
      const response = await fetch(`/api/lineups/wide?game_id=${gameId}&player_id=${playerId}`);
      const data: { lineups: Lineup[] } = await response.json();
      setStints(data.lineups.map((lineup) => ({
        period: lineup.period,
        startTime: lineup.time_in,
        endTime: lineup.time_out,
      })));
    } catch (error) {
      console.error('Error fetching player stints:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Game Stints</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="col-span-1">
          <h2 className="text-xl font-semibold mb-2">Players</h2>
          <ul className="bg-white shadow-md rounded-lg overflow-hidden">
            {players.map((player) => (
              <li
                key={player.id}
                className={`p-2 cursor-pointer hover:bg-gray-100 ${
                  selectedPlayer?.id === player.id ? 'bg-blue-100' : ''
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
          {selectedPlayer && (
            <PlayerStint
              playerName={selectedPlayer.name}
              playerPosition={selectedPlayer.position}
              stints={stints}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default GameStintsPage;
