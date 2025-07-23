"use client"
import React, { useState} from "react";
import {PlusIcon} from "@heroicons/react/24/solid";


interface Task {
    id: number;
    name: string;
    status: boolean;
}
interface Props {
    tasks: Task[];
    handlerAdd: () => void;
    handleSearch: (value: string) => void;
    setApiSelection: (useDjango: boolean) => void;
}
const SearchBar = ({tasks, handlerAdd,handleSearch, setApiSelection}: Props) => {
    const [searchTask, setSearchTask] = useState<string>("")


    const onChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        const value=e.target.value
        setSearchTask(value);
        handleSearch(value)
        console.log("filter task", tasks)
    }

    return (
        <div className="w-full border border-gray-300 rounded-md p-2 bg-white shadow-sm flex gap-4 items-center ">
            <input
                type="text"
                className="flex-1 border border-gray-300 rounded px-2 py-1 text-sm p-0.5"
                placeholder="Search Task"
                value={searchTask}
                onChange={onChange}
            />
            <div className="flex space-x-2 items-center">
                <button className="bg-green-500 hover:bg-green-600 text-white p-2 rounded cursor-pointer">
                    <PlusIcon className="h-4 w-4" onClick={handlerAdd}/>
                </button>
                <button className="bg-yellow-400 hover:bg-yellow-600 text-white p-2 rounded cursor-pointer" onClick={()=>{setApiSelection(false)}}>
                   FLASK
                </button>
                <button className="bg-green-950 hover:bg-green-600 text-white p-2 rounded cursor-pointer" onClick={()=>{setApiSelection(true)}}>
                   DJANGO
                </button>
            </div>
        </div>
    );
};

export default SearchBar;
