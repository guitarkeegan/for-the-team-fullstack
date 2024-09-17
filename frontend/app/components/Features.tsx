"use client";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from 'next/navigation';

interface FeatureProps {
  title: string;
  imageSrc: string;
  coachLink: string;
  medicalLink: string;
}

export function FeatureCard({ title, imageSrc, coachLink, medicalLink }: FeatureProps) {
  const pathname = usePathname();
  const link = pathname.startsWith('/coach-dash') ? coachLink : medicalLink;

  return (
    <Link href={link} className="block">
      <div className="relative w-64 h-64 rounded-full overflow-hidden group cursor-pointer">
        <Image
          src={imageSrc}
          alt={title}
          layout="fill"
          objectFit="cover"
          className="group-hover:scale-110 transition-transform duration-300"
        />
        <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center group-hover:bg-opacity-50 transition-all duration-300">
          <h2 className="text-white text-2xl font-heading text-center px-4">{title}</h2>
        </div>
      </div>
    </Link>
  );
}

export default function Features() {
  const features = [
    { 
      title: "Team Schedule", 
      imageSrc: "/images/player-performance.webp", 
      coachLink: "/coach-dash/team-schedule",
      medicalLink: "/medical-dash/team-schedule"
    },
    { 
      title: "Team Strategy", 
      imageSrc: "/images/team-strategy.webp", 
      coachLink: "#",
      medicalLink: "#"
    },
    { 
      title: "Training Schedule", 
      imageSrc: "/images/training-schedule.webp", 
      coachLink: "#",
      medicalLink: "#"
    },
  ];

  return (
    <div className="flex flex-wrap justify-center gap-8 p-8">
      {features.map((feature, index) => (
        <FeatureCard key={index} {...feature} />
      ))}
    </div>
  );
}