import Link from "next/link";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-2">
          Documentation Analyzer
        </h1>
        <p className="text-muted-foreground">
          Analyze and fix documentation quality issues with 18 specialized modules
        </p>
      </header>

      <div className="bg-card rounded-lg border p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-4">Get Started</h2>
        <p className="text-muted-foreground mb-4">
          Ready to analyze your documentation? Start by configuring your analysis settings.
        </p>
        <Link
          href="/analyze"
          className="inline-block px-6 py-3 bg-primary text-primary-foreground rounded-md font-semibold hover:opacity-90"
        >
          Start Analysis
        </Link>
      </div>

      <div className="mt-8 bg-secondary rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-3">System Capabilities</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-background rounded p-4">
            <h4 className="font-semibold mb-2">📊 18 Analyzers</h4>
            <p className="text-sm text-muted-foreground">
              Core, high-impact, and advanced analysis modules
            </p>
          </div>
          <div className="bg-background rounded p-4">
            <h4 className="font-semibold mb-2">🔧 18 Fixers</h4>
            <p className="text-sm text-muted-foreground">
              Automatic and semi-automatic fixes
            </p>
          </div>
          <div className="bg-background rounded p-4">
            <h4 className="font-semibold mb-2">🤖 AI-Powered</h4>
            <p className="text-sm text-muted-foreground">
              Claude AI integration for style validation
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
