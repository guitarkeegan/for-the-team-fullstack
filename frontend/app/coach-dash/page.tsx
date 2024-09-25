"use client";
import Features from "@/app/components/Features";
import { useAuth } from "../hooks/useAuth";
import { useRouter } from "next/navigation";

export default function CoachDash() {
  const { user, loading } = useAuth();
  const router = useRouter();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user || !user.roles.includes("coach")) {
    router.replace("/login");
    return null;
  }

  return (
    <div className="p-4 bg-teamSilver flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-5xl font-heading text-teamBlue mb-8">
        Coaches Dashboard
      </h1>
      <Features />
    </div>
  );
}
