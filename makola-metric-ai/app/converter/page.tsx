"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { Loader2, ArrowRightLeft, Zap } from "lucide-react";
import ProtectedRoute from "@/components/ProtectedRoute";

const CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "MXN"];

export default function ConverterPage() {
  const router = useRouter();
  const [sourceValue, setSourceValue] = useState("");
  const [sourceCurrency, setSourceCurrency] = useState("USD");
  const [targetCurrency, setTargetCurrency] = useState("EUR");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const swapCurrencies = () => {
    setSourceCurrency(targetCurrency);
    setTargetCurrency(sourceCurrency);
    setResult(null);
  };

  const handleConvert = async () => {
    if (!sourceValue || isNaN(parseFloat(sourceValue))) {
      toast.error("Please enter a valid amount");
      return;
    }

    setIsLoading(true);

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }

      const response = await fetch("/api/conversions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          sourceValue: parseFloat(sourceValue),
          sourceCurrency,
          targetCurrency,
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem("token");
          router.push("/login");
          return;
        }
        const error = await response.json();
        toast.error(error.detail || "Conversion failed");
        return;
      }

      const data = await response.json();
      setResult(data);
      toast.success("Conversion successful!");
    } catch (error) {
      toast.error("Failed to convert. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-foreground mb-2">Currency Converter</h1>
            <p className="text-foreground/70">
              Convert currencies with AI-powered confidence scoring
            </p>
          </div>

          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Convert Currency</CardTitle>
              <CardDescription>
                Enter the amount and select currencies to convert
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Amount Input */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Amount</label>
                  <Input
                    type="number"
                    placeholder="Enter amount"
                    value={sourceValue}
                    onChange={(e) => setSourceValue(e.target.value)}
                    disabled={isLoading}
                    step="0.01"
                  />
                </div>

                {/* Currency Selection */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-foreground">From</label>
                    <Select value={sourceCurrency} onValueChange={setSourceCurrency} disabled={isLoading}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {CURRENCIES.map((curr) => (
                          <SelectItem key={curr} value={curr}>
                            {curr}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-foreground">To</label>
                    <div className="relative">
                      <Select value={targetCurrency} onValueChange={setTargetCurrency} disabled={isLoading}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {CURRENCIES.map((curr) => (
                            <SelectItem key={curr} value={curr}>
                              {curr}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={swapCurrencies}
                        disabled={isLoading}
                        className="absolute right-1 top-1/2 -translate-y-1/2"
                      >
                        <ArrowRightLeft className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>

                {/* Convert Button */}
                <Button
                  onClick={handleConvert}
                  disabled={isLoading || !sourceValue}
                  className="w-full"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Converting...
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4 mr-2" />
                      Convert Now
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Result Card */}
          {result && (
            <Card className="border-2 border-primary/20 bg-primary/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="w-5 h-5 text-primary" />
                  Conversion Result
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Main Result */}
                <div className="bg-background rounded-lg p-6 text-center">
                  <p className="text-foreground/70 text-sm mb-2">
                    {sourceValue} {sourceCurrency}
                  </p>
                  <h2 className="text-4xl font-bold text-foreground mb-2">
                    {parseFloat(result.resultValue).toFixed(2)}
                  </h2>
                  <p className="text-foreground/70 text-sm">
                    {result.targetCurrency}
                  </p>
                </div>

                {/* Conversion Rate */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-background rounded-lg p-4">
                    <p className="text-foreground/60 text-sm mb-1">Exchange Rate</p>
                    <p className="text-xl font-semibold text-foreground">
                      1 {sourceCurrency} = {parseFloat(result.conversionRate).toFixed(4)} {targetCurrency}
                    </p>
                  </div>

                  <div className="bg-background rounded-lg p-4">
                    <p className="text-foreground/60 text-sm mb-1">AI Confidence</p>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-background border rounded-full h-2">
                        <div
                          className="bg-primary rounded-full h-full transition-all"
                          style={{ width: `${result.confidence}%` }}
                        />
                      </div>
                      <p className="text-xl font-semibold text-foreground w-12 text-right">
                        {result.confidence.toFixed(1)}%
                      </p>
                    </div>
                  </div>
                </div>

                {/* Market Conditions */}
                {result.metadata && (
                  <div className="bg-background rounded-lg p-4">
                    <p className="text-foreground/60 text-sm mb-3">Market Conditions</p>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-foreground/70">Market Condition:</span>
                        <span className="font-semibold text-foreground capitalize">
                          {result.metadata.marketCondition}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-foreground/70">Data Recency:</span>
                        <span className="font-semibold text-foreground">
                          Current
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Timestamp */}
                <p className="text-xs text-foreground/50 text-center">
                  Converted on {new Date(result.createdAt).toLocaleString()}
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
