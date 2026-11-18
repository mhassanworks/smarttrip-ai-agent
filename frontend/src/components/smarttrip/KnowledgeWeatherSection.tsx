import React, { useState, useEffect } from "react";
import { fetchWeather } from "../../services/smarttripApi";

export const KnowledgeWeatherSection: React.FC = () => {
  const [city, setCity] = useState("Goa");
  const [weatherData, setWeatherData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const cities = ["Goa", "Delhi", "Mumbai", "Jaipur", "Bengaluru", "Manali"];

  const loadWeather = async (cityName: string) => {
    setLoading(true);
    try {
      const data = await fetchWeather(cityName);
      setWeatherData(data);
    } catch (err) {
      console.error("Weather fetch error", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWeather(city);
  }, [city]);

  const profile = weatherData?.knowledge_profile;
  const weather = weatherData?.current_weather;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-1">
            Assignment 8 &middot; Knowledge Base & Open-Meteo API
          </div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>Destination Ontology & Real-Time Weather Integration</span>
            {loading && <span className="text-sm font-normal text-indigo-400 animate-pulse">(Updating...)</span>}
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Structured JSON knowledge representation linked with live Open-Meteo REST API forecasts and seamless mock fallback.
          </p>
        </div>

        {/* City selector pills */}
        <div className="flex flex-wrap gap-1.5 bg-slate-800/80 p-1 rounded-xl border border-slate-700">
          {cities.map((c) => (
            <button
              key={c}
              onClick={() => setCity(c)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                city === c ? "bg-indigo-600 text-white shadow" : "text-slate-400 hover:text-white"
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {/* Weather & Live Advisory Banner */}
      {weather && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Temperature & Condition */}
          <div className="bg-gradient-to-br from-indigo-950/80 to-slate-900 border border-indigo-500/30 rounded-2xl p-6">
            <div className="flex items-center justify-between text-xs font-medium text-indigo-300">
              <span>LIVE WEATHER &middot; {profile?.city_name?.toUpperCase()}</span>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Source: {weatherData.data_source}
              </span>
            </div>
            <div className="flex items-baseline gap-3 mt-4">
              <span className="text-5xl font-extrabold text-white">
                {weather.temperature_celsius}&deg;C
              </span>
              <span className="text-sm text-slate-300 font-medium">
                {weather.condition}
              </span>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-400 mt-4 pt-3 border-t border-slate-800 font-mono">
              <span>Wind: {weather.windspeed_kmh} km/h</span>
              <span>&middot;</span>
              <span>Suitability: {Math.round(weather.suitability_score * 100)}%</span>
            </div>
          </div>

          {/* Travel Advisory */}
          <div className="md:col-span-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 mb-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                AUTOMATED WEATHER ADVISORY & RECOMMENDATION
              </div>
              <p className="text-sm text-slate-200 leading-relaxed font-sans mt-2">
                {weatherData.travel_advisory}
              </p>
            </div>

            <div className="flex flex-wrap gap-2 mt-4 pt-3 border-t border-slate-800 text-xs text-slate-400 font-mono">
              <span>Coords: {weatherData.coordinates?.latitude}&deg;N, {weatherData.coordinates?.longitude}&deg;E</span>
              <span>&middot;</span>
              <span>Outdoor Sights: {weather.is_outdoor_recommended ? "RECOMMENDED" : "CAUTION"}</span>
            </div>
          </div>
        </div>
      )}

      {/* Structured Destination Knowledge Profile */}
      {profile && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Metadata Card */}
          <div className="lg:col-span-4 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h3 className="text-base font-semibold text-white border-b border-slate-800 pb-3">
              Ontological Profile: {profile.city_name}
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 block">Region & IATA Code</span>
                <span className="text-white font-semibold font-mono text-sm">{profile.state_country} ({profile.iata_code})</span>
              </div>

              <div>
                <span className="text-slate-400 block">Best Travel Season</span>
                <span className="text-emerald-300 font-medium">{profile.best_season}</span>
              </div>

              <div>
                <span className="text-slate-400 block">Climate Zone</span>
                <span className="text-slate-200 font-medium">{profile.climate_zone}</span>
              </div>

              <div>
                <span className="text-slate-400 block">Average Daily Budget</span>
                <span className="text-white font-mono font-bold">₹{profile.average_daily_budget_inr?.toLocaleString()} / day</span>
              </div>

              <div>
                <span className="text-slate-400 block mb-1">Culinary Highlights</span>
                <div className="flex flex-wrap gap-1.5">
                  {profile.culinary_highlights?.map((food: string, i: number) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-slate-800 text-indigo-300 font-medium">
                      {food}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800">
                <span className="text-slate-400 block mb-1">Local Transit Tips</span>
                <p className="text-slate-300 leading-relaxed text-[11px] italic">
                  &ldquo;{profile.travel_tips}&rdquo;
                </p>
              </div>
            </div>
          </div>

          {/* Key Attractions Table */}
          <div className="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-base font-semibold text-white mb-3">
              Curated Attractions & Entry Fee Knowledge Registry
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
                    <th className="py-2.5 px-3">Landmark / Monument</th>
                    <th className="py-2.5 px-3">Category</th>
                    <th className="py-2.5 px-3 text-right">Entry Fee (INR)</th>
                    <th className="py-2.5 px-3 text-right">Duration</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {profile.key_attractions?.map((att: any, i: number) => (
                    <tr key={i} className="hover:bg-slate-800/40">
                      <td className="py-3 px-3 font-semibold text-white">{att.name}</td>
                      <td className="py-3 px-3 text-indigo-300">{att.type}</td>
                      <td className="py-3 px-3 text-right font-mono font-bold text-emerald-400">
                        {att.est_fee_inr === 0 ? "FREE" : `₹${att.est_fee_inr}`}
                      </td>
                      <td className="py-3 px-3 text-right font-mono text-slate-400">{att.avg_time_hours} hrs</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
