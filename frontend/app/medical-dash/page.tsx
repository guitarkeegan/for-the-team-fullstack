import Features from "../components/Features";

export default function MedicalDashboard() {
  return (
    <div className="p-4 bg-teamSilver flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-5xl font-heading text-teamBlue mb-8">Medical Dashboard</h1>
      <Features />
    </div>
  );
}