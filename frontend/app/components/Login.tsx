"use client";
import { useRouter } from "next/navigation";    
import { useState } from "react";
export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const router = useRouter();

  // TODO: implement auth!
  const user1 = {
    username: "user_one",
    password: "password123",
  };

  const user2 = {
    username: "user_two",
    password: "123password",
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (username === user1.username && password === user1.password) {
      router.replace("/coach-dash");
    } else if (username === user2.username && password === user2.password) {
      router.replace("/medical-dash");
    } else {
        setErrorMsg("Invalid email or password");
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
