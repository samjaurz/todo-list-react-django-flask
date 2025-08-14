import NavBar from "@/components/NavBar";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <NavBar />
      <div className="flex-grow flex items-center justify-center p-4">
        <div className="max-w-4xl w-full grid md:grid-cols-2 gap-12 items-center">
          <div className="flex flex-col justify-center space-y-4">
            <h1 className="text-5xl font-bold text-gray-800">TODO LIST</h1>
            <p className="text-xl text-gray-600">
              Add task
            </p>
            <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-8 rounded-lg w-fit transition shadow-md hover:shadow-lg">
              SIGN UP
            </button>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md flex justify-center">
            <img
              src="https://illustrations.popsy.co/amber/task-list.svg"
              alt="Ilustración de lista de tareas"
              className="w-full h-auto max-w-xs"
            />
          </div>
        </div>
      </div>
    </div>
  );
}