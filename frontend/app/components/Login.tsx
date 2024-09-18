"use client";
import { useRouter } from "next/navigation";    
import { useState } from "react";
import { setToken } from '../utils/api';

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const credentials = Buffer.from(`${username}:${password}`).toString('base64');
      const response = await fetch('/api/user/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Basic ${credentials}`
        },
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();

      // Use the new token key
      setToken(data['for-the-team-token']);

      // Decode the JWT to get the user's role
      const [, payload] = data['for-the-team-token'].split('.');
      const decodedPayload = JSON.parse(Buffer.from(payload, 'base64').toString('utf-8'));
      const userRole = decodedPayload.role;

      // Redirect based on user role
      if (userRole === 'COACH') {
        router.replace("/coach-dash");
      } else if (userRole === 'MEDICAL') {
        router.replace("/medical-dash");
      } else {
        setErrorMsg("Unknown user role");
      }
    } catch (error) {
      setErrorMsg("Invalid username or password");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {errorMsg && <p className="text-red-500">{errorMsg}</p>}
      <div>
        <label
          htmlFor="username"
          className="block text-sm font-medium text-gray-700"
        >
          Username
        </label>
        <input
          type="text"
          id="username"
          name="username"
          onChange={(e) => setUsername(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-md focus:border-teamBlue focus:ring focus:ring-teamBlue focus:ring-opacity-50 text-gray-800 font-sans"
        />
      </div>
      <div>
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700"
        >
          Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-md focus:border-teamBlue focus:ring focus:ring-teamBlue focus:ring-opacity-50 text-gray-800 font-sans"
        />
      </div>
      <button
        type="submit"
        className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teamRed hover:bg-teamBlue focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teamBlue"
      >
        Log In
      </button>
    </form>
  );
}
