import { useEffect, useState } from 'react';
import { teamService, leaveService, payrollService, timeTrackingService } from '../services/api';

interface TeamMember {
  id: string;
  name: string;
  role: string;
}

interface DashboardData {
  teamMembers: TeamMember[];
  leaveRequests: {
    id: string;
    employeeId?: string | number;
    startDate?: string;
    endDate?: string;
    status: string;
  }[];
  payroll: {
    employeeId?: string | number;
    salary: number;
    payrollDate: string;
    deductions: number;
  }[];
  timeTracking: {
    id: string;
    employeeId?: string | number;
    clockIn: string;
    clockOut: string;
    totalHours: number;
  }[];
}

export const Dashboard = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [teamResponse, rawLeave, rawPayroll, rawTimeTracking] = await Promise.all([
          teamService.getTeamMembers(),
          leaveService.getAllLeaveRequests(),
          payrollService.getAllPayrollData(),
          timeTrackingService.getAllTimeTracking(),
        ]);

        const leaveResponse = rawLeave.map((item: any) => ({
          ...item,
          employeeId: item.employee_id,
          startDate: item.start_date,
          endDate: item.end_date,
        }));

        const payrollResponse = rawPayroll.map((item: any) => ({
          ...item,
          employeeId: item.employee_id,
        }));

        const timeTrackingResponse = rawTimeTracking.map((item: any) => ({
          ...item,
          employeeId: item.employee_id,
          clockIn: item.clock_in,
          clockOut: item.clock_out,
          totalHours: item.total_hours,
        }));

        const team = teamResponse as TeamMember[];
        const uniqueTeam = Array.from(new Map(team.map(emp => [emp.id, emp])).values());

        setData({
          teamMembers: uniqueTeam,
          leaveRequests: leaveResponse,
          payroll: payrollResponse,
          timeTracking: timeTrackingResponse,
        });
      } catch (error) {
        console.error('Fehler beim Laden der Dashboard-Daten:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getEmployeeName = (id?: string | number) => {
    if (!id || !data?.teamMembers) return 'Unbekannt';
    const emp = data.teamMembers.find(e => String(e.id) === String(id));
    return emp?.name?.trim() || `Mitarbeiter (ID: ${id})`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Team Members</h2>
          <div className="space-y-4">
            {data?.teamMembers.map((member) => (
              <div key={member.id} className="flex flex-col">
                <p className="font-medium text-sm">{member.name}</p>
                <p className="text-xs text-gray-500">{member.role}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Leave Requests</h2>
          <div className="space-y-4">
            {data?.leaveRequests.map((leave) => (
              <div key={leave.id} className="border-b pb-4 last:border-0">
                {leave.startDate && leave.endDate && !isNaN(Date.parse(leave.startDate)) && !isNaN(Date.parse(leave.endDate)) ? (
                  <p className="text-sm text-gray-600">
                    {getEmployeeName(leave.employeeId)} is on leave from{' '}
                    {new Date(leave.startDate).toLocaleDateString()} to{' '}
                    {new Date(leave.endDate).toLocaleDateString()}
                  </p>
                ) : (
                  <p className="text-sm text-red-500">
                    Invalid leave data for {getEmployeeName(leave.employeeId)}
                  </p>
                )}
                <span className="text-xs text-gray-400">{leave.status}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Payroll</h2>
          <div className="space-y-4">
            {data?.payroll.map((payroll, idx) => (
              <div key={idx} className="border-b pb-4 last:border-0">
                <p className="text-sm text-gray-600">
                  {getEmployeeName(payroll.employeeId)} earned ${payroll.salary} this month.
                </p>
                <span className="text-xs text-gray-400">Deductions: ${payroll.deductions}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Time Tracking</h2>
          <div className="space-y-4">
            {data?.timeTracking.map((entry) => (
              <div key={entry.id} className="border-b pb-4 last:border-0">
                <p className="text-sm text-gray-600">
                  {getEmployeeName(entry.employeeId)} clocked in at{' '}
                  {new Date(entry.clockIn).toLocaleTimeString()} and out at{' '}
                  {new Date(entry.clockOut).toLocaleTimeString()}.
                </p>
                <span className="text-xs text-gray-400">Total Hours: {entry.totalHours}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
