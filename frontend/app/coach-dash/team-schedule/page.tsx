'use client';
import React, { useEffect, useState } from 'react';
import GameCard from '../../components/GameCard';
import { useRouter } from 'next/navigation';

interface Game {
  away_id: number;
  away_name: string;
  away_score: number;
  game_date: string;
  game_id: number;
  home_id: number;
  home_name: string;
  home_score: number;
}

// Function to group games by month
const groupGamesByMonth = (games: Game[]) => {
  const grouped = games.reduce((acc, game) => {
    const date = new Date(game.game_date);
    const monthYear = date.toLocaleString('default', { month: 'long', year: 'numeric' });
    if (!acc[monthYear]) {
      acc[monthYear] = [];
    }
    acc[monthYear].push(game);
    return acc;
  }, {} as Record<string, Game[]>);

  return Object.entries(grouped).sort(([a], [b]) => 
    new Date(a).getTime() - new Date(b).getTime()
  );
};

export default function TeamSchedule() {
  const [games, setGames] = useState<Game[]>([]);
  const router = useRouter();

  useEffect(() => {
    const fetchGames = async () => {
      const teamId = process.env.NEXT_PUBLIC_TEAM_ID;
      const year = new Date().getFullYear();
      const response = await fetch(`/api/schedule/past-games/${teamId}/${year}`);
      const data = await response.json();
      setGames(data);
    };

    fetchGames();
  }, []);

  const groupedGames = groupGamesByMonth(games);

  const handleGameClick = (game: Game) => {
    const searchParams = new URLSearchParams({
      homeTeam: game.home_name,
      awayTeam: game.away_name,
      homeScore: game.home_score.toString(),
      awayScore: game.away_score.toString(),
      homeId: game.home_id.toString(),
      awayId: game.away_id.toString(),
    });
    router.push(`/coach-dash/game-stints/${game.game_id}?${searchParams.toString()}`);
  };

  return (
    <div className="p-4 bg-teamSilver">
      <h1 className="text-4xl font-heading text-teamBlue mb-8 text-center">Team Schedule</h1>
      {groupedGames.map(([monthYear, monthGames]) => (
        <div key={monthYear} className="mb-8">
          <h2 className="text-2xl font-heading text-teamRed mb-4">{monthYear}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {monthGames.map((game) => (
              <GameCard
                    key={game.game_id}
                    date={new Date(game.game_date).toLocaleDateString()}
                    homeTeam={{ name: game.home_name, score: game.home_score }}
                    awayTeam={{ name: game.away_name, score: game.away_score }}
                    onClick={() => handleGameClick(game)}
                    id={game.game_id.toString()}
                  />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
