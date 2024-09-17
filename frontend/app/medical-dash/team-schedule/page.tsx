import React from 'react';
import GameCard from '../../components/GameCard';

// Mock data for past games
const pastGames = [
  {
    date: "2023-10-15",
    homeTeam: { name: "LA Clippers", score: 105 },
    awayTeam: { name: "Portland Trail Blazers", score: 98 }
  },
  {
    date: "2023-10-20",
    homeTeam: { name: "LA Lakers", score: 110 },
    awayTeam: { name: "LA Clippers", score: 115 }
  },
  {
    date: "2023-11-05",
    homeTeam: { name: "LA Clippers", score: 120 },
    awayTeam: { name: "Golden State Warriors", score: 112 }
  },
  // Add more past games here...
];

// Function to group games by month
const groupGamesByMonth = (games: typeof pastGames) => {
  const grouped = games.reduce((acc, game) => {
    const date = new Date(game.date);
    const monthYear = date.toLocaleString('default', { month: 'long', year: 'numeric' });
    if (!acc[monthYear]) {
      acc[monthYear] = [];
    }
    acc[monthYear].push(game);
    return acc;
  }, {} as Record<string, typeof pastGames>);

  return Object.entries(grouped).sort(([a], [b]) => 
    new Date(a).getTime() - new Date(b).getTime()
  );
};

export default function TeamSchedule() {
  const groupedGames = groupGamesByMonth(pastGames);

  return (
    <div className="p-4 bg-teamSilver">
      <h1 className="text-4xl font-heading text-teamBlue mb-8 text-center">Team Schedule</h1>
      {groupedGames.map(([monthYear, games]) => (
        <div key={monthYear} className="mb-8">
          <h2 className="text-2xl font-heading text-teamRed mb-4">{monthYear}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {games.map((game, index) => (
              <GameCard key={index} {...game} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}