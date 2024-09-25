"use client";
import { useRouter } from "next/navigation";    
import { useState, useEffect } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [csrfToken, setCsrfToken] = useState("");
  const router = useRouter();

  useEffect(() => {
    fetch('/api/get-csrf-token', {
      credentials: 'include',
    })
      .then(response => response.json())
      .then(data => setCsrfToken(data.csrf_token))
      .catch(error => console.error('Error fetching CSRF token:', error));
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const loginResponse = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
      });

      if (loginResponse.ok) {
        // Fetch user info after successful login
        const userInfoResponse = await fetch('/api/user-info', {
          credentials: 'include',
        });

        if (userInfoResponse.ok) {
          const userData = await userInfoResponse.json();
          if (userData.roles.includes('coach')) {
            router.replace("/coach-dash");
          } else if (userData.roles.includes('medical')) {
            router.replace("/medical-dash");
          } else {
            setErrorMsg("Unknown user role");
          }
        } else {
          setErrorMsg("Failed to fetch user information");
        }
      } else {
        setErrorMsg("Invalid email or password");
      }
    } catch (error) {
      console.error('Login error:', error);
      setErrorMsg("An error occurred. Please try again.");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {errorMsg && <p className="text-red-500">{errorMsg}</p>}
      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700"
        >
          Email
        </label>
        <input
          type="email"
          id="email"
          name="email"
          onChange={(e) => setEmail(e.target.value)}
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
