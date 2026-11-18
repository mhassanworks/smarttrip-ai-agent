import { useState } from "react";
import { Header, type DashboardTab } from "./components/Header";
import { Footer } from "./components/Footer";
import { TripRequestForm } from "./components/TripRequestForm";
import { AgentProgress } from "./components/AgentProgress";
import { ItineraryLoadingSkeleton } from "./components/ItineraryLoadingSkeleton";
import { ItineraryView } from "./components/ItineraryView";
import { PlanningError } from "./components/PlanningError";
import { SavedTrips } from "./components/SavedTrips";
import { useTripPlannerSSE } from "./hooks/useTripPlannerSSE";
import { useSavedTrips } from "./hooks/useSavedTrips";
import type { TripRequest, Itinerary } from "./types/trip";

// SmartTrip Multi-Agent Modules
import { SystemOverviewSection } from "./components/smarttrip/SystemOverviewSection";
import { PeasSection } from "./components/smarttrip/PeasSection";
import { RuleEngineSection } from "./components/smarttrip/RuleEngineSection";
import { ConcurrencySection } from "./components/smarttrip/ConcurrencySection";
import { SocketCommSection } from "./components/smarttrip/SocketCommSection";
import { NegotiationSection } from "./components/smarttrip/NegotiationSection";
import { UtilityOptimizerSection } from "./components/smarttrip/UtilityOptimizerSection";
import { BdiSection } from "./components/smarttrip/BdiSection";
import { KnowledgeWeatherSection } from "./components/smarttrip/KnowledgeWeatherSection";
import { SecuritySection } from "./components/smarttrip/SecuritySection";
import { CapstoneDemoSection } from "./components/smarttrip/CapstoneDemoSection";

function App() {
  const { phase, board, timeline, itinerary: plannedItinerary, errorMessage, planTrip, reset } = useTripPlannerSSE();
  const { fetchTrip } = useSavedTrips();
  const [destination, setDestination] = useState("");
  const [activeTab, setActiveTab] = useState<DashboardTab>("overview");
  const [plannerSubView, setPlannerSubView] = useState<"new-trip" | "my-trips">("new-trip");
  const [viewedItinerary, setViewedItinerary] = useState<Itinerary | null>(null);

  const handleSubmit = (request: TripRequest) => {
    setDestination(request.destination);
    setViewedItinerary(null);
    setPlannerSubView("new-trip");
    planTrip(request);
  };

  const handleTabChange = (tab: DashboardTab) => {
    setActiveTab(tab);
    if (tab === "trip-planner") {
      setPlannerSubView("new-trip");
    }
  };

  const handleViewTrip = async (id: string) => {
    const trip = await fetchTrip(id);
    if (trip) {
      reset();
      setViewedItinerary(trip);
      setActiveTab("trip-planner");
      setPlannerSubView("new-trip");
    }
  };

  const showLoadingSkeleton = phase === "planning" && plannedItinerary !== null;
  const activeItinerary = viewedItinerary || plannedItinerary;

  return (
    <div className="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      <Header
        activeTab={activeTab}
        onTabChange={handleTabChange}
        onLaunchDemo={() => setActiveTab("demo")}
      />

      <main className="flex-1 max-w-[1536px] w-full mx-auto px-4 sm:px-6 py-6 md:py-8">
        {/* SECTION 1: OVERVIEW & SYSTEM HEALTH */}
        {activeTab === "overview" && (
          <SystemOverviewSection
            onNavigate={handleTabChange}
            onLaunchDemo={() => setActiveTab("demo")}
          />
        )}

        {/* SECTION 2: TRIP PLANNER (LANGGRAPH SSE WORKFLOW) */}
        {activeTab === "trip-planner" && (
          <div className="space-y-6">
            <div className="flex items-center justify-between bg-slate-900/90 border border-slate-800 p-4 rounded-xl">
              <div className="flex items-center gap-2 text-xs">
                <button
                  onClick={() => {
                    setPlannerSubView("new-trip");
                    setViewedItinerary(null);
                  }}
                  className={`px-3 py-1.5 rounded-lg font-medium cursor-pointer ${
                    plannerSubView === "new-trip"
                      ? "bg-indigo-600 text-white"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Create Plan
                </button>
                <button
                  onClick={() => setPlannerSubView("my-trips")}
                  className={`px-3 py-1.5 rounded-lg font-medium cursor-pointer ${
                    plannerSubView === "my-trips"
                      ? "bg-indigo-600 text-white"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Saved SQLite Trips
                </button>
              </div>

              <span className="text-xs text-indigo-400 font-mono hidden sm:inline">
                Live SSE Stream: /plan-trip
              </span>
            </div>

            {plannerSubView === "my-trips" ? (
              <SavedTrips
                onViewTrip={handleViewTrip}
                onCreateNew={() => setPlannerSubView("new-trip")}
              />
            ) : (
              <>
                {phase === "idle" && !viewedItinerary && (
                  <TripRequestForm onSubmit={handleSubmit} isSubmitting={false} />
                )}

                {phase === "planning" && !showLoadingSkeleton && (
                  <AgentProgress destination={destination} board={board} timeline={timeline} />
                )}

                {showLoadingSkeleton && <ItineraryLoadingSkeleton />}

                {(phase === "complete" || viewedItinerary) && activeItinerary && (
                  <ItineraryView
                    itinerary={activeItinerary}
                    onPlanAnother={() => {
                      reset();
                      setViewedItinerary(null);
                    }}
                  />
                )}

                {phase === "error" && (
                  <PlanningError
                    message={errorMessage ?? "Something went wrong. Please try again."}
                    onRetry={reset}
                  />
                )}
              </>
            )}
          </div>
        )}

        {/* SECTION 3: PEAS & AGENT PERSONAS */}
        {activeTab === "peas" && <PeasSection />}

        {/* SECTION 4: CONDITION-ACTION RULE ENGINE */}
        {activeTab === "rules" && <RuleEngineSection />}

        {/* SECTION 5: MULTI-AGENT NEGOTIATION */}
        {activeTab === "negotiation" && <NegotiationSection />}

        {/* SECTION 6: UTILITY OPTIMIZATION (10 CONFIGS) */}
        {activeTab === "utility" && <UtilityOptimizerSection />}

        {/* SECTION 7: BDI DYNAMIC REPLANNING */}
        {activeTab === "bdi" && <BdiSection />}

        {/* SECTION 8: KNOWLEDGE BASE & OPEN-METEO WEATHER */}
        {activeTab === "knowledge" && <KnowledgeWeatherSection />}

        {/* SECTION 9: TCP SOCKET COMMUNICATION */}
        {activeTab === "socket" && <SocketCommSection />}

        {/* SECTION 10: CRYPTOGRAPHIC SECURITY & HMAC */}
        {activeTab === "security" && <SecuritySection />}

        {/* SECTION 11: CONCURRENCY WORKERS & LATENCY */}
        {activeTab === "workers" && <ConcurrencySection />}

        {/* SECTION 12: CAPSTONE LIFECYCLE & DEMO MODE */}
        {activeTab === "demo" && <CapstoneDemoSection />}
      </main>

      <Footer
        note={
          activeItinerary?.best_effort
            ? `Best effort — couldn't fully fit budget after ${activeItinerary.negotiation_rounds} rounds of rebalancing.`
            : "SmartTrip AI &middot; Autonomous Multi-Agent Travel Planning &amp; Negotiation System"
        }
      />
    </div>
  );
}

export default App;
