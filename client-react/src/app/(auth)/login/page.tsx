"use client";
import getApiInstance from "@/lib/axios";
import {useRouter} from "next/navigation";
import React, {useState} from "react";

export default function LoginPage() {

    // const [apiSelection, setApiSelection] = useState(false)
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const api = getApiInstance(false);
    const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const payload = {
            "email": email,
            "password": password
        }
        const response = await api.post('auth/login', payload);
        console.log("response from login", response.data)

        if (response.status === 200) {
        router.push("/tasks");
      } else {
      console.log("Not authorized");
    }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6 text-center">Log In</h2>
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Email</label>
                        <input
                            type="email"
                            className="mt-1 block w-full px-4 py-2 border rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none"
                            placeholder="email@email.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required

                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Password</label>
                        <input
                            type="password"
                            className="mt-1 block w-full px-4 py-2 border rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required

                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full py-2 px-4 rounded-lg shadow text-white bg-gray-800 hover:bg-gray-700"
                    >
                        Log In
                    </button>
                </form>

                <p className="mt-4 text-center text-sm text-gray-600">
                    Don’t have an account?{" "}
                    <a href="/signup" className="text-blue-600 hover:underline">
                        Sign Up
                    </a>
                </p>
            </div>
        </div>
    );
}
