import React from "react";

interface Player {
  name: string;
  team: string;
  position: string;
}

interface BasketballCourtProps {
  players: Player[];
}

const TShirt: React.FC<{ color: string }> = ({ color }) => (
  <path
    d="M -12,0 L -10,-8 C -10,-12 -5,-15 0,-15 C 5,-15 10,-12 10,-8 L 12,0 L 10,15 C 8,17 4,18 0,18 C -4,18 -8,17 -10,15 Z"
    fill={color}
    stroke="#ffffff"
    strokeWidth="1"
  />
);

const PlayerIcon: React.FC<{ player: Player; x: number; y: number }> = ({
  player,
  x,
  y,
}) => (
  <g transform={`translate(${x}, ${y})`}>
    <TShirt color={player.team === "home" ? "#ff0000" : "#0000ff"} />
    <text
      x="0"
      y="25"
      textAnchor="middle"
      fill="#000"
      fontSize="16"
      fontFamily="Arial, sans-serif"
      fontWeight="bolder"
    >
      {player.name}
    </text>
  </g>
);

export default function BasketballCourt({ players }: BasketballCourtProps) {
  const clippersTeamId = process.env.NEXT_PUBLIC_TEAM_ID || "";
  console.log("clippersTeamId", clippersTeamId);
  console.log("players on court", players);
  const clippersPlayers = players.filter((player) => player.team === "home");
  const otherTeamPlayers = players.filter((player) => player.team === "away");

  // Predefined positions for 5 players on each half-court
  const leftPositions = [
    { x: 80, y: 225 },
    { x: 220, y: 225 },
    { x: 150, y: 175 },
    { x: 80, y: 125 },
    { x: 220, y: 125 },
  ];

  const rightPositions = [
    { x: 350, y: 75 },
    { x: 500, y: 75 },
    { x: 425, y: 125 },
    { x: 350, y: 175 },
    { x: 500, y: 175 },
  ];

  return (
    <svg width="600" height="300" viewBox="0 0 600 300">
      {/* Court background */}
      <rect x="0" y="0" width="600" height="300" fill="#cd9b5a" />

      {/* Key areas */}
      <rect x="0" y="75" width="190" height="150" fill="#b7864e" />
      <rect x="410" y="75" width="190" height="150" fill="#b7864e" />

      {/* Court outline */}
      <rect
        x="0"
        y="0"
        width="600"
        height="300"
        fill="none"
        stroke="#ffffff"
        strokeWidth="2"
      />

      {/* Center circle */}
      <circle
        cx="300"
        cy="150"
        r="60"
        fill="none"
        stroke="#ffffff"
        strokeWidth="2"
      />

      {/* Center line */}
      <line
        x1="300"
        y1="0"
        x2="300"
        y2="300"
        stroke="#ffffff"
        strokeWidth="2"
      />

      {/* Three-point lines */}
      <path
        d="M 0,35 Q 190,35 190,150 Q 190,265 0,265"
        fill="none"
        stroke="#ffffff"
        strokeWidth="2"
      />
      <path
        d="M 600,35 Q 410,35 410,150 Q 410,265 600,265"
        fill="none"
        stroke="#ffffff"
        strokeWidth="2"
      />

      {/* Free throw circles */}
      <circle
        cx="125"
        cy="150"
        r="60"
        fill="none"
        stroke="#ffffff"
        strokeWidth="2"
      />
      <circle
        cx="475"
        cy="150"
        r="60"
        fill="none"
        stroke="#ffffff"
        strokeWidth="2"
      />

      {/* Free throw lines */}
      <line x1="0" y1="75" x2="190" y2="75" stroke="#ffffff" strokeWidth="2" />
      <line
        x1="0"
        y1="225"
        x2="190"
        y2="225"
        stroke="#ffffff"
        strokeWidth="2"
      />
      <line
        x1="410"
        y1="75"
        x2="600"
        y2="75"
        stroke="#ffffff"
        strokeWidth="2"
      />
      <line
        x1="410"
        y1="225"
        x2="600"
        y2="225"
        stroke="#ffffff"
        strokeWidth="2"
      />

      {/* Backboards */}
      <line
        x1="30"
        y1="100"
        x2="30"
        y2="200"
        stroke="#ffffff"
        strokeWidth="4"
      />
      <line
        x1="570"
        y1="100"
        x2="570"
        y2="200"
        stroke="#ffffff"
        strokeWidth="4"
      />

      {/* Hoops */}
      <circle
        cx="30"
        cy="150"
        r="7.5"
        fill="none"
        stroke="#ff7f00"
        strokeWidth="2"
      />
      <circle
        cx="570"
        cy="150"
        r="7.5"
        fill="none"
        stroke="#ff7f00"
        strokeWidth="2"
      />

      {/* Players */}
      {clippersPlayers.map((player, index) => (
        <PlayerIcon
          key={`clippers-${index}`}
          player={player}
          x={leftPositions[index % 5].x}
          y={leftPositions[index % 5].y}
        />
      ))}
      {otherTeamPlayers.map((player, index) => (
        <PlayerIcon
          key={`other-${index}`}
          player={player}
          x={rightPositions[index % 5].x}
          y={rightPositions[index % 5].y}
        />
      ))}
    </svg>
  );
}
