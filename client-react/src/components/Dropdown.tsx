import React, {useState} from "react";

interface User {
    id: number,
    name: string,
    last_name: string,
    status: boolean
}

interface Props {
    users: User[];
    handleFilterUser: (user: User) => void;
}

const Dropdown = ({users, handleFilterUser}: Props) => {
    console.log(users)
    const [selectedValue, setSelectedValue] = useState('');

    const handleChange = (event) => {
        const value=event.target.value
        setSelectedValue(value);
        handleFilterUser(value)
        console.log(value,"prin valut")
  };
    return (

        <div>
            <select value={selectedValue} onChange={handleChange}>
                <option value="all">Select a user</option>
                {users.map((users) => (
                    <option key={users.id} value={users.id}>
                        {users.name}
                    </option>
                ))}
            </select>
        </div>
    )
};

export default Dropdown;


//
// <div>
//     <select value={selectedValue} onChange={handleChange}>
//         <option value="">Select a fruit</option>
//         {/* Default/placeholder option */}
//         {options.map((option) => (
//             <option key={option.value} value={option.value}>
//                 {option.label}
//             </option>
//         ))}
//     </select>
//     <p>Selected: {selectedValue}</p>
// </div>