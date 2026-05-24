"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Loader2, Trash2, ChevronLeft, ChevronRight } from "lucide-react";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function HistoryPage() {
  const router = useRouter();
  const [conversions, setConversions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadConversions();
  }, [page]);

  const loadConversions = async () => {
    setIsLoading(true);

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }

      const response = await fetch(`/api/conversions?page=${page}&pageSize=10`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push("/login");
          return;
        }
        throw new Error("Failed to load conversions");
      }

      const data = await response.json();
      setConversions(data.items);
      setTotal(data.total);
    } catch (error) {
      toast.error("Failed to load conversion history");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this conversion?")) return;

    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`/api/conversions/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete conversion");
      }

      toast.success("Conversion deleted");
      setConversions(conversions.filter((c) => c.id !== id));
    } catch (error) {
      toast.error("Failed to delete conversion");
    }
  };

  const pageSize = 10;
  const totalPages = Math.ceil(total / pageSize);

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-foreground mb-2">Conversion History</h1>
            <p className="text-foreground/70">
              View and manage your past currency conversions
            </p>
          </div>

          {isLoading ? (
            <Card>
              <CardContent className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-foreground/40" />
              </CardContent>
            </Card>
          ) : conversions.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <p className="text-foreground/60 mb-4">No conversions yet</p>
                <Button onClick={() => router.push("/converter")}>
                  Create Your First Conversion
                </Button>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="space-y-4 mb-8">
                {conversions.map((conversion) => (
                  <Card key={conversion.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6">
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                        {/* Conversion Details */}
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <div className="text-right">
                              <p className="font-semibold text-foreground">
                                {parseFloat(conversion.sourceValue).toFixed(2)}
                              </p>
                              <p className="text-xs text-foreground/60">
                                {conversion.sourceCurrency}
                              </p>
                            </div>
                            <span className="text-foreground/40">→</span>
                            <div>
                              <p className="font-semibold text-foreground">
                                {parseFloat(conversion.resultValue).toFixed(2)}
                              </p>
                              <p className="text-xs text-foreground/60">
                                {conversion.targetCurrency}
                              </p>
                            </div>
                          </div>
                          <p className="text-xs text-foreground/50">
                            {new Date(conversion.createdAt).toLocaleString()}
                          </p>
                        </div>

                        {/* Confidence Score */}
                        <div className="flex items-center gap-2 sm:w-32">
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-foreground/60">Confidence</span>
                              <span className="text-xs font-semibold text-foreground">
                                {conversion.confidence.toFixed(1)}%
                              </span>
                            </div>
                            <div className="bg-background border rounded-full h-2">
                              <div
                                className="bg-primary rounded-full h-full transition-all"
                                style={{ width: `${conversion.confidence}%` }}
                              />
                            </div>
                          </div>
                        </div>

                        {/* Delete Button */}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(conversion.id)}
                          className="text-destructive hover:text-destructive"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(Math.max(1, page - 1))}
                    disabled={page === 1}
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </Button>

                  <span className="text-sm text-foreground/70">
                    Page {page} of {totalPages}
                  </span>

                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(Math.min(totalPages, page + 1))}
                    disabled={page === totalPages}
                  >
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
