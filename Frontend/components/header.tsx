import { Building2 } from "lucide-react"

export function Header() {
  return (
    <header className="border-b border-border bg-card">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
            <Building2 className="w-6 h-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-foreground">Bank of Maharashtra</h1>
            <p className="text-xs text-muted-foreground">Loan Product Assistant</p>
          </div>
        </div>
        <div className="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
          <a href="#" className="hover:text-foreground transition-colors">
            Home Loans
          </a>
          <a href="#" className="hover:text-foreground transition-colors">
            Personal Loans
          </a>
          <a href="#" className="hover:text-foreground transition-colors">
            About
          </a>
        </div>
      </div>
    </header>
  )
}
