"use client"
import NavBar from "@/components/NavBar"
import getApiInstance from "@/lib/axios";
import {useSearchParams, useRouter} from 'next/navigation'

const Verification = () => {
    const searchParams = useSearchParams()
    const verification_token: string | null = searchParams.get('token')
    const user_email: string | null = searchParams.get("email");
    const api = getApiInstance(false);
    const router = useRouter()

    if (verification_token) {
        sessionStorage.setItem('access_token', verification_token);
        console.log(verification_token);}

    const handleVerification = async () => {
        try {
            const response = await api.get('/auth/verification');
            if (response.status == 200) {
                console.log(response);
                router.push("/tasks");
            }
        } catch (error) {
            console.error("Error Axios", error);
            console.log("error from not getting task")
            router.push("/");
            return null;
        }
    }

    const handleResendEmail = async () => {
        try {
            const payload = {
                email: user_email
            }
            const response = await api.post('auth/resend_email_verification', payload);
            if (response.status == 200) {
                console.log(response.data);
            }
        } catch (error) {
            console.error("Error Axios", error);
            console.log("error from not getting task")
        }
    }


    return (
        <div className="min-h-screen bg-gray-50">
            <NavBar/>
            <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
                <h1 className="text-2xl font-bold text-center mb-4">Confirm email address</h1>
                <p className="text-gray-600 text-center mb-6">
                    Verify your email. We sent you an email with a link to verify your account.
                </p>
                <button
                    className="bg-green-700 hover:bg-green-800 text-white font-medium py-2 px-4 rounded cursor-pointer transition-colors"
                    onClick={handleResendEmail}>
                    RESEND EMAIL
                </button>
                <button
                    className="bg-green-700 hover:bg-green-800 text-white font-medium py-2 px-4 rounded cursor-pointer transition-colors"
                    onClick={handleVerification}>
                    CONFIRM EMAIL
                </button>
            </div>
        </div>
    )
}

export default Verification