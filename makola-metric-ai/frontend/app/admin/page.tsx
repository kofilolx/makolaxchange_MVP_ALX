'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { getAdminStats, getAdminUsers } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';
import Navigation from '@/components/Navigation';

interface AdminStats {
  totalUsers: number;
  totalConversions: number;
  totalVolume: number;
  avgConfidence: number;
}

interface AdminUser {
  id: string;
  email: string;
  name: string;
  conversionsCount: number;
  createdAt: string;
}

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (authLoading) return;

    const loadData = async () => {
      try {
        const [statsData, usersData] = await Promise.all([
          getAdminStats(),
          getAdminUsers(),
        ]);
        setStats(statsData);
        setUsers(usersData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load admin data');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [authLoading]);

  if (authLoading || loading) {
    return (
      <ProtectedRoute requiredRole="admin">
        <Navigation />
        <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-6">
          <div className="max-w-6xl mx-auto">
            <div className="text-center text-white">Loading admin dashboard...</div>
          </div>
        </main>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute requiredRole="admin">
      <Navigation />
      <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">Admin Dashboard</h1>
            <p className="text-slate-400">System overview and user management</p>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 mb-6 text-red-300">
              {error}
            </div>
          )}

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="text-sm text-slate-400 mb-2">Total Users</div>
              <div className="text-3xl font-bold text-white">{stats?.totalUsers ?? 0}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="text-sm text-slate-400 mb-2">Total Conversions</div>
              <div className="text-3xl font-bold text-white">{stats?.totalConversions ?? 0}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="text-sm text-slate-400 mb-2">Total Volume</div>
              <div className="text-3xl font-bold text-white">
                ${(stats?.totalVolume ?? 0).toFixed(2)}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="text-sm text-slate-400 mb-2">Avg Confidence</div>
              <div className="text-3xl font-bold text-white">
                {((stats?.avgConfidence ?? 0) * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Users Table */}
          <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
            <div className="p-6 border-b border-slate-700">
              <h2 className="text-xl font-bold text-white">User Management</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-700/50">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-300">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-300">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-300">
                      Conversions
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-slate-300">
                      Joined
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="px-6 py-8 text-center text-slate-400">
                        No users found
                      </td>
                    </tr>
                  ) : (
                    users.map((u) => (
                      <tr key={u.id} className="hover:bg-slate-700/30">
                        <td className="px-6 py-4 text-white">{u.name}</td>
                        <td className="px-6 py-4 text-slate-300">{u.email}</td>
                        <td className="px-6 py-4 text-slate-300">{u.conversionsCount}</td>
                        <td className="px-6 py-4 text-slate-400">
                          {new Date(u.createdAt).toLocaleDateString()}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </ProtectedRoute>
  );
}
