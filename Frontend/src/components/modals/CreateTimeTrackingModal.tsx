import { useState } from "react";
import { timeTrackingService } from "../../services/api";

export const CreateTimeTrackingModal = ({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: () => void;
}) => {
  const [employeeId, setEmployeeId] = useState("");
  const [clockIn, setClockIn] = useState("");
  const [clockOut, setClockOut] = useState("");
  const [totalHours, setTotalHours] = useState("");

  const handleSubmit = async () => {
    if (!employeeId || !clockIn || !clockOut || !totalHours) return;

    try {
      await timeTrackingService.addTimeTracking(
        employeeId,
        clockIn,
        clockOut,
        parseFloat(totalHours)
      );
      alert("Time tracking entry added successfully.");
      onCreated();
      onClose();
    } catch (error) {
      console.error("Error adding time tracking entry:", error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-md w-full max-w-md">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">
          Add Time Tracking Entry
        </h2>

        <input
          type="text"
          placeholder="Employee ID"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="datetime-local"
          value={clockIn}
          onChange={(e) => setClockIn(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="datetime-local"
          value={clockOut}
          onChange={(e) => setClockOut(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="number"
          placeholder="Total Hours"
          value={totalHours}
          onChange={(e) => setTotalHours(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <div className="flex justify-end space-x-2">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm bg-gray-300 dark:bg-gray-600 rounded"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={
              !employeeId || !clockIn || !clockOut || !totalHours
            }
            className={`px-4 py-2 text-sm text-white rounded ${
              !employeeId || !clockIn || !clockOut || !totalHours
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};
