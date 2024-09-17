"use client";
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Period from '@/app/components/Period';
import TimeRange from '@/app/components/TimeRange';
import BasketballCourt from '@/app/components/BasketballCourt';

// Define types for our data
type Player = {
  name: string;
  team: string;
  position: string;
};

// Update the Stint type to match the API response
type Stint = {
  id: number;
  period: number;
  startTime: number;
  endTime: number;
  players: Player[];
};

type StintsByPeriod = {
  [key: number]: Stint[];
};

export default function GameStints({ params }: { params: { gameId: string } }) {
  const [activePeriod, setActivePeriod] = useState(1);
  const [activeStint, setActiveStint] = useState<number | null>(null);
  const [stintsByPeriod, setStintsByPeriod] = useState<StintsByPeriod>({});
  const periods = [1, 2, 3, 4];

  const searchParams = useSearchParams();
  const homeTeam = searchParams.get('homeTeam') || '';
  const awayTeam = searchParams.get('awayTeam') || '';
  const homeScore = searchParams.get('homeScore') || '';
  const awayScore = searchParams.get('awayScore') || '';

  useEffect(() => {
    const fetchStintData = async () => {
      try {
        console.log('Fetching stint data for game:', params.gameId);
        const response = await fetch(`/api/lineups/wide?game_id=${params.gameId}`);
        const data = await response.json();
        console.log('Received stint data:', data);
        
        const processedStints = processStints(data.lineups);
        setStintsByPeriod(processedStints);
      } catch (error) {
        console.error('Error fetching stint data:', error);
      }
    };

    fetchStintData();
  }, [params.gameId]);

  const processStints = (lineups: any[]): StintsByPeriod => {
    const stintsByPeriod: StintsByPeriod = {};
    lineups.forEach((lineup, index) => {
      const period = lineup.period;
      // Convert time to seconds from start of period (720 seconds = 12 minutes)
      const startTime = 720 - parseFloat(lineup.time_in);
      const endTime = 720 - parseFloat(lineup.time_out);

      const players: Player[] = [
        { name: lineup.player1_name, position: lineup.player1_position, team: lineup.team_id === parseInt(params.gameId.split('-')[0]) ? 'home' : 'away' },
        { name: lineup.player2_name, position: lineup.player2_position, team: lineup.team_id === parseInt(params.gameId.split('-')[0]) ? 'home' : 'away' },
        { name: lineup.player3_name, position: lineup.player3_position, team: lineup.team_id === parseInt(params.gameId.split('-')[0]) ? 'home' : 'away' },
        { name: lineup.player4_name, position: lineup.player4_position, team: lineup.team_id === parseInt(params.gameId.split('-')[0]) ? 'home' : 'away' },
        { name: lineup.player5_name, position: lineup.player5_position, team: lineup.team_id === parseInt(params.gameId.split('-')[0]) ? 'home' : 'away' },
      ];

      const processedStint: Stint = {
        id: index,
        period,
        startTime,
        endTime,
        players,
      };

      if (!stintsByPeriod[period]) {
        stintsByPeriod[period] = [];
      }
      stintsByPeriod[period].push(processedStint);
    });

    // Sort stints within each period by startTime
    for (const period in stintsByPeriod) {
      stintsByPeriod[period].sort((a, b) => a.startTime - b.startTime);
    }

    console.log('Processed stintsByPeriod:', stintsByPeriod);
    return stintsByPeriod;
  };

  // Add this logging
  useEffect(() => {
    console.log('Current stintsByPeriod:', stintsByPeriod);
  }, [stintsByPeriod]);

  const activePlayers = activeStint !== null && stintsByPeriod[activePeriod]
    ? stintsByPeriod[activePeriod].find(stint => stint.id === activeStint)?.players || []
    : [];

  return (
    <div className="p-4 bg-teamSilver flex flex-col items-center gap-4">
      <h1 className="text-4xl font-heading text-teamBlue mb-8 text-center">Game Stints</h1>
      
      <div className="w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px] mb-8">
        <div className="flex justify-between items-center w-full">
          <h2 className="text-2xl font-heading text-teamRed">{homeTeam}</h2>
          <div className="text-3xl font-bold">
            {homeScore} - {awayScore}
          </div>
          <h2 className="text-2xl font-heading text-teamRed">{awayTeam}</h2>
        </div>
      </div>

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
      
      {/* Add this conditional rendering and error message */}
      {Object.keys(stintsByPeriod).length === 0 ? (
        <p>No stint data available. Please check the console for any errors.</p>
      ) : (
        <>
          <div className="mb-8 flex justify-center w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px]">
            <BasketballCourt players={activePlayers} />
          </div>
          <div className="flex flex-wrap justify-center gap-2 mb-8 w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px]">
            {stintsByPeriod[activePeriod]?.map((stint) => (
              <TimeRange
                key={stint.id}
                startTime={stint.startTime}
                endTime={stint.endTime}
                isActive={activeStint === stint.id}
                onClick={() => setActiveStint(stint.id)}
              />
            ))}
          </div>
        </>
      )}
      
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
