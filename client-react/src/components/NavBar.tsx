'use client'
import React from "react";
import {useRouter} from "next/navigation";

const Navbar = () => {
    const router = useRouter();
    return (
        <nav className="flex items-center justify-between p-4 bg-gray-800 text-white shadow-md">
            <h1 className="text-xl font-bold">TODO LIST</h1>

            <div className="flex space-x-3">
                <button
                    onClick={() => router.push("/login")}
                    className="px-4 py-2 rounded border border-white hover:bg-gray-700 transition"
                >
                    Login
                </button>
                <button
                    onClick={() => router.push("/signup")}
                    className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded cursor-pointer transition"
                >

                    Signup
                </button>
                <button
                    onClick={() => router.push("/signup")}
                    className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded cursor-pointer transition"
                >
                    Sign Out
                </button>
            </div>
        </nav>
    );
};

export default Navbar;