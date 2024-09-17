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

interface PlayerStintChartProps {
  playerName: string;
  stints: {
    periodStart: number;
    startTime: number;
    endTime: number;
  }[];
  periods?: number;
  periodLength?: number;
}

const PlayerStintChart: React.FC<PlayerStintChartProps> = ({
  playerName,
  stints,
  periods = 4,
  periodLength = 12,
}) => {
  const width = 240;
  const height = 600;
  const chartWidth = 60;
  const periodHeight = height / periods;
  const secondsPerPixel = (periodLength * 60) / periodHeight;
  const bracketWidth = 10;

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
      .toString()
      .padStart(2, "0")}`;
  };

  const getStintColor = (periodStart: number, startTime: number) => {
    const totalSeconds = (periodStart - 1) * periodLength * 60 + startTime;
    const maxSeconds = periods * periodLength * 60;
    const percentage = totalSeconds / maxSeconds;

    // Sky Blue RGB: 135, 206, 235
    // Crimson Red RGB: 220, 20, 60
    const r = Math.round(135 + (220 - 135) * percentage);
    const g = Math.round(206 + (20 - 206) * percentage);
    const b = Math.round(235 + (60 - 235) * percentage);

    return `rgb(${r}, ${g}, ${b})`;
  };

  return (
    <svg
      width={width}
      height={height + 40}
      viewBox={`0 0 ${width} ${height + 40}`}
    >
      <text
        x={width / 2}
        y="20"
        textAnchor="middle"
        fontSize="16"
        fontWeight="bold"
      >
        {playerName}
      </text>

      {/* Chart background */}
      <rect
        x={(width - chartWidth) / 2}
        y="40"
        width={chartWidth}
        height={height}
        fill="white"
        stroke="gray"
      />

      {/* Period lines, labels, and brackets */}
      {[...Array(periods)].map((_, index) => (
        <React.Fragment key={index}>
          <line
            x1={(width - chartWidth) / 2}
            y1={40 + index * periodHeight}
            x2={(width + chartWidth) / 2}
            y2={40 + index * periodHeight}
            stroke="gray"
          />
          <text
            x={width - 10}
            y={40 + index * periodHeight + periodHeight / 2}
            textAnchor="end"
            dominantBaseline="middle"
            fontSize="12"
          >
            Period {index + 1}
          </text>
          {/* Left bracket */}
          <path
            d={`M ${(width - chartWidth) / 2 - bracketWidth} ${
              40 + index * periodHeight
            } 
                 h ${bracketWidth} 
                 v ${periodHeight} 
                 h -${bracketWidth}`}
            fill="none"
            stroke="black"
            strokeWidth="2"
          />
          {/* Right bracket */}
          <path
            d={`M ${(width + chartWidth) / 2 + bracketWidth} ${
              40 + index * periodHeight
            } 
                 h -${bracketWidth} 
                 v ${periodHeight} 
                 h ${bracketWidth}`}
            fill="none"
            stroke="black"
            strokeWidth="2"
          />
        </React.Fragment>
      ))}

      {/* Stints */}
      {stints.map((stint, index) => {
        const y1 =
          40 +
          (stint.periodStart - 1) * periodHeight +
          stint.startTime / secondsPerPixel;
        const y2 =
          40 +
          (stint.periodStart - 1) * periodHeight +
          stint.endTime / secondsPerPixel;
        return (
          <React.Fragment key={index}>
            <rect
              x={(width - chartWidth) / 2}
              y={y1}
              width={chartWidth}
              height={y2 - y1}
              fill={getStintColor(stint.periodStart, stint.startTime)}
              opacity="0.75"
            />
            <text
              x={(width - chartWidth) / 2 - 5}
              y={y1}
              textAnchor="end"
              dominantBaseline="middle"
              fontSize="10"
            >
              {formatTime(stint.startTime)}
            </text>
            <text
              x={(width - chartWidth) / 2 - 5}
              y={y2}
              textAnchor="end"
              dominantBaseline="middle"
              fontSize="10"
            >
              {formatTime(stint.endTime)}
            </text>
          </React.Fragment>
        );
      })}
    </svg>
  );
};

const convertTimeToSeconds = (time: string): number => {
  const [minutes, seconds] = time.split(':').map(Number);
  return minutes * 60 + seconds;
};

const PlayerStint: React.FC<PlayerStintProps> = ({ playerName, playerPosition, stints }) => {
  const convertedStints = stints.map(stint => ({
    periodStart: stint.period,
    startTime: convertTimeToSeconds(stint.startTime),
    endTime: convertTimeToSeconds(stint.endTime),
  }));

  return (
    <div className="flex flex-col items-center bg-white p-4 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-2">{playerName} - {playerPosition}</h3>
      <PlayerStintChart
        playerName={playerName}
        stints={convertedStints}
        periods={4}
        periodLength={12}
      />
    </div>
  );
};

export default PlayerStint;
