import React from "react";

interface Stint {
  period: number;
  startTime: string;
  endTime: string;
}

interface PlayerStintProps {
  playerName: string;
  playerPosition: string;
  stints: Stint[];
}

const PlayerStint: React.FC<PlayerStintProps> = ({ playerName, playerPosition, stints }) => {
  const maxPeriod = Math.max(...stints.map(stint => stint.period), 4); // Ensure at least 4 periods are shown

  const periodBlocks = Array.from({ length: maxPeriod }, (_, i) => i + 1).map(period => {
    const periodStints = stints.filter(stint => stint.period === period);
    return (
      <div key={period} className="flex flex-col mb-2">
        <div className="font-semibold mb-1">Period {period}</div>
        <div className="h-8 bg-gray-200 relative">
          {periodStints.map((stint, index) => {
            const startPercent = (parseFloat(stint.startTime) / 720) * 100;
            const endPercent = (parseFloat(stint.endTime) / 720) * 100;
            const width = startPercent - endPercent;
            return (
              <div
                key={index}
                className="absolute h-full bg-blue-500"
                style={{
                  left: `${endPercent}%`,
                  width: `${width}%`,
                }}
              ></div>
            );
          })}
        </div>
      </div>
    );
  });

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-lg font-semibold mb-2">{playerName} ({playerPosition})</h3>
      {periodBlocks}
    </div>
  );
};

export default PlayerStint;
