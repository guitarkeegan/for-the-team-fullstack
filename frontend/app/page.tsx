import Image from "next/image";
import Login from "./components/Login";
export default function Home() {
  return (
    <main className="min-h-screen bg-teamSilver flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-96 flex flex-col items-center gap-4">
        <h1 className="text-3xl font-bold text-teamBlue mb-6 text-center">Welcome</h1>
        <Image src="/clippers-logo.png" alt="logo" width={100} height={100} />
        <Login />
      </div>
    </main>
  );
}
