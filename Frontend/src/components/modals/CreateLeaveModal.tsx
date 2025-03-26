// src/components/modals/CreateLeaveModal.tsx
import { useState } from "react";
import { leaveService } from "../../services/api";

export const CreateLeaveModal = ({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) => {
  const [employeeId, setEmployeeId] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [status, setStatus] = useState("Pending");

  const handleSubmit = async () => {
    if (!employeeId || !startDate || !endDate) return;
  
    try {
      await leaveService.requestLeave(employeeId, startDate, endDate, status);
      alert("Leave request saved successfully."); 
      onCreated();   // Dashboard aktualisieren
      onClose();     // Modal schließen
    } catch (error) {
      console.error("Error while saving leave request:", error);
    }
  };
  
  

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-md w-full max-w-md">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">Add Leave Request</h2>
        <input
          type="text"
          placeholder="Employee ID"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        >
          <option>Pending</option>
          <option>Approved</option>
          <option>Rejected</option>
        </select>
        <div className="flex justify-end space-x-2">
          <button onClick={onClose} className="px-4 py-2 text-sm bg-gray-300 dark:bg-gray-600 rounded">Cancel</button>
          <button onClick={handleSubmit} className="px-4 py-2 text-sm bg-blue-600 text-white rounded">Save</button>
        </div>
      </div>
    </div>
  );
};
