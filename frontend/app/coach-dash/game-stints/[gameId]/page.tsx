"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Period from "@/app/components/Period";
import TimeRange from "@/app/components/TimeRange";
import BasketballCourt from "@/app/components/BasketballCourt";

// Define types for our data
type Player = {
  name: string;
  team: string;
  position: string;
};

// Update the Stint type to include both teams
type Stint = {
  id: number;
  period: number;
  startTime: number;
  endTime: number;
  homePlayers: Player[];
  awayPlayers: Player[];
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
  const homeTeam = searchParams.get("homeTeam") || "";
  const awayTeam = searchParams.get("awayTeam") || "";
  const homeScore = searchParams.get("homeScore") || "";
  const awayScore = searchParams.get("awayScore") || "";

  const [clippersTeamId, setClippersTeamId] = useState<string>("");

  useEffect(() => {
    setClippersTeamId(process.env.NEXT_PUBLIC_TEAM_ID || "");
  }, []);

  useEffect(() => {
    const fetchStintData = async () => {
      try {
        console.log("Fetching stint data for game:", params.gameId);
        const response = await fetch(
          `/api/lineups/wide?game_id=${params.gameId}`,
          {
            credentials: "include",
          }
        );
        const data = await response.json();
        console.log("Received stint data:", data);

        const processedStints = processStints(data.lineups);
        setStintsByPeriod(processedStints);
      } catch (error) {
        console.error("Error fetching stint data:", error);
      }
    };
    fetchStintData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.gameId, clippersTeamId]);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const processStints = (lineups: any[]): StintsByPeriod => {
    const stintsByPeriod: StintsByPeriod = {};
    const stintMap: { [key: string]: Stint } = {};

    lineups.forEach((lineup) => {
      const period = lineup.period;
      const startTime = 720 - parseFloat(lineup.time_in);
      const endTime = 720 - parseFloat(lineup.time_out);
      const isHomeTeam = lineup.team_id.toString() === clippersTeamId;

      const players: Player[] = [
        {
          name: lineup.player1_name,
          position: lineup.player1_position || "UNKNOWN",
          team: isHomeTeam ? "home" : "away",
        },
        {
          name: lineup.player2_name,
          position: lineup.player2_position || "UNKNOWN",
          team: isHomeTeam ? "home" : "away",
        },
        {
          name: lineup.player3_name,
          position: lineup.player3_position || "UNKNOWN",
          team: isHomeTeam ? "home" : "away",
        },
        {
          name: lineup.player4_name,
          position: lineup.player4_position || "UNKNOWN",
          team: isHomeTeam ? "home" : "away",
        },
        {
          name: lineup.player5_name,
          position: lineup.player5_position || "UNKNOWN",
          team: isHomeTeam ? "home" : "away",
        },
      ];

      const stintKey = `${period}-${startTime}-${endTime}`;
      if (!stintMap[stintKey]) {
        stintMap[stintKey] = {
          id: Object.keys(stintMap).length,
          period,
          startTime,
          endTime,
          homePlayers: isHomeTeam ? players : [],
          awayPlayers: isHomeTeam ? [] : players,
        };
      } else {
        if (isHomeTeam) {
          stintMap[stintKey].homePlayers = players;
        } else {
          stintMap[stintKey].awayPlayers = players;
        }
      }
    });

    // Convert stintMap to array and sort by period and startTime
    const sortedStints = Object.values(stintMap).sort((a, b) => {
      if (a.period !== b.period) return a.period - b.period;
      return a.startTime - b.startTime;
    });

    // Group stints by period
    sortedStints.forEach((stint) => {
      if (!stintsByPeriod[stint.period]) {
        stintsByPeriod[stint.period] = [];
      }
      stintsByPeriod[stint.period].push(stint);
    });

    console.log("Processed stintsByPeriod:", stintsByPeriod);
    return stintsByPeriod;
  };

  useEffect(() => {
    console.log("Current stintsByPeriod:", stintsByPeriod);
    console.log("Active Period:", activePeriod);
    console.log("Active Stint:", activeStint);
  }, [stintsByPeriod, activePeriod, activeStint]);

  const getBothTeamsPlayers = () => {
    if (activeStint === null || !stintsByPeriod[activePeriod]) return [];
    const stint = stintsByPeriod[activePeriod].find(
      (s) => s.id === activeStint
    );
    if (!stint) return [];
    return [...stint.homePlayers, ...stint.awayPlayers];
  };

  const isClippersHome =
    parseInt(params.gameId.split("-")[0]) === parseInt(clippersTeamId);

  return (
    <div className="p-4 bg-teamSilver flex flex-col items-center gap-4">
      <h1 className="text-4xl font-heading text-teamBlue mb-8 text-center">
        Game Stints
      </h1>

      <div className="w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px] mb-8">
        <div className="flex justify-between items-center w-full">
          <h2 className="text-2xl font-heading text-red-600">
            {isClippersHome ? homeTeam : awayTeam}{" "}
            {/* Clippers always on the left */}
          </h2>
          <div className="text-3xl font-bold">
            {isClippersHome ? homeScore : awayScore} -{" "}
            {isClippersHome ? awayScore : homeScore}
          </div>
          <h2 className="text-2xl font-heading text-blue-600">
            {isClippersHome ? awayTeam : homeTeam}{" "}
            {/* Opposing team always on the right */}
          </h2>
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

      {Object.keys(stintsByPeriod).length === 0 ? (
        <p>No stint data available. Please check the console for any errors.</p>
      ) : (
        <>
          <div className="mb-8 flex justify-center w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px]">
            <BasketballCourt players={getBothTeamsPlayers()} />
          </div>
          <div className="flex flex-wrap justify-center gap-2 mb-8 w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px]">
            {stintsByPeriod[activePeriod]?.map((stint) => (
              <TimeRange
                key={stint.id}
                startTime={stint.startTime}
                endTime={stint.endTime}
                isActive={activeStint === stint.id}
                onClick={() => {
                  setActiveStint(stint.id);
                  console.log("Set Active Stint:", stint.id);
                }}
              />
            ))}
          </div>
          {activeStint !== null && (
            <div className="w-full max-w-[600px] md:max-w-[800px] lg:max-w-[1000px]">
              <h3 className="text-2xl font-heading text-teamBlue mb-4">
                Active Players
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="text-xl font-heading text-teamRed mb-2">
                    Clippers
                  </h4>
                  {getBothTeamsPlayers()
                    .filter((player) => player.team === "home")
                    .map((player, index) => (
                      <p key={index} className="mb-1">
                        {player.name} - {player.position}
                      </p>
                    ))}
                </div>
                <div>
                  <h4 className="text-xl font-heading text-teamRed mb-2">
                    Opposing Team
                  </h4>
                  {getBothTeamsPlayers()
                    .filter((player) => player.team === "away")
                    .map((player, index) => (
                      <p key={index} className="mb-1">
                        {player.name} - {player.position}
                      </p>
                    ))}
                </div>
              </div>
            </div>
          )}
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
