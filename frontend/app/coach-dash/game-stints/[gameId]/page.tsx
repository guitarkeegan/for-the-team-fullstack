"use client";
import React, { useState } from 'react';
import Period from '@/app/components/Period';
import TimeRange from '@/app/components/TimeRange';
import BasketballCourt from '@/app/components/BasketballCourt';

// Mock data for stints and players
const stintsByPeriod = {
  1: [
    { id: 1, startTime: 720, endTime: 600, players: [
      { name: "Player 1", x: 100, y: 70 },
      { name: "Player 2", x: 200, y: 50 },
      { name: "Player 3", x: 300, y: 70 },
      { name: "Player 4", x: 150, y: 140 },
      { name: "Player 5", x: 250, y: 140 },
      { name: "Player 6", x: 300, y: 230 },
      { name: "Player 7", x: 400, y: 250 },
      { name: "Player 8", x: 500, y: 230 },
      { name: "Player 9", x: 350, y: 160 },
      { name: "Player 10", x: 450, y: 160 },
    ]},
    { id: 2, startTime: 600, endTime: 480, players: [
      // Different player positions for this stint
    ]},
    // ... other stints
  ],
  2: [
    { id: 7, startTime: 720, endTime: 540, players: [
      // Player positions for first stint of second period
    ]},
    // ... other stints
  ],
  // ... periods 3 and 4
};

export default function GameStints({ params }: { params: { gameId: string } }) {
  const [activePeriod, setActivePeriod] = useState(1);
  const [activeStint, setActiveStint] = useState<number | null>(null);
  const periods = [1, 2, 3, 4];

//   const activePlayers = activeStint
//     ? stintsByPeriod[activePeriod as keyof typeof stintsByPeriod].find(stint => stint.id === activeStint)?.players
//     : [];

  return (
    <div className="p-4 bg-teamSilver">
      <h1 className="text-4xl font-heading text-teamBlue mb-8 text-center">Game Stints</h1>
      <p className="text-xl mb-4">Game ID: {params.gameId}</p>
      <div className="flex justify-center space-x-4 mb-8">
        {periods.map((period) => (
          <Period
            key={period}
            number={period}
            isActive={activePeriod === period}
            onClick={() => {
              setActivePeriod(period);
              setActiveStint(null);
            }}
          />
        ))}
      </div>
      <div className="mb-8 flex justify-center">
        <BasketballCourt />
      </div>
      <div className="flex flex-wrap justify-center gap-2 mb-8">
        {stintsByPeriod[activePeriod as keyof typeof stintsByPeriod].map((stint) => (
          <TimeRange
            key={stint.id}
            startTime={stint.startTime}
            endTime={stint.endTime}
            isActive={activeStint === stint.id}
            onClick={() => setActiveStint(stint.id)}
          />
        ))}
      </div>
      <div>
        <p className="text-center text-xl">
          {activeStint 
            ? `Showing details for stint ${activeStint} in period ${activePeriod}` 
            : `Select a stint for period ${activePeriod}`}
        </p>
      </div>
    </div>
  );
}
