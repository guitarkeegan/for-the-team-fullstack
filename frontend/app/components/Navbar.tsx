"use client";
import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const router = useRouter();

    const handleLogout = () => {
        // Here you would typically handle the logout logic
        // For now, we'll just redirect to the homepage
        router.push('/');
    };

    return (
        <nav className="bg-teamBlue p-4 flex justify-end items-center relative">
            <div className="relative">
                <button 
                    onClick={() => setIsOpen(!isOpen)} 
                    className="focus:outline-none"
                >
                    <Image src="/clippers-logo.png" alt="logo" width={50} height={50} />
                </button>
                {isOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                        <button 
                            onClick={handleLogout}
                            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        >
                            Log out
                        </button>
                    </div>
                )}
            </div>
        </nav>
    );
}