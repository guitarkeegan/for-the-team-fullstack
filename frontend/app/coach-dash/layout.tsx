import Navbar from "../components/Navbar";

export default function CoachDashboardLayout({
    children, // will be a page or nested layout
  }: {
    children: React.ReactNode
  }) {
    return (
      <div className="bg-teamSilver">
        <Navbar />
        {children}
      </div>
    )
  }