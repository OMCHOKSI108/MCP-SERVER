from graphviz import Digraph
import os
import platform

def create_workflow_diagram():
    """Generates a visual diagram of the AI agent's workflow."""
    
    # Check if Graphviz is available
    try:
        # Try to create a simple test diagram to verify Graphviz is working
        test_dot = Digraph()
        test_dot.node('test', 'test')
        test_dot.source  # This will work if graphviz python package is installed
        
        # Try to render to check if system Graphviz is available
        test_dot.render('temp_test', format='png', cleanup=True)
        
    except Exception as e:
        print("❌ Graphviz system binaries not found or not in PATH!")
        print("\n📋 To fix this:")
        
        if platform.system() == "Windows":
            print("1. Install Graphviz: winget install Graphviz.Graphviz")
            print("2. Add to PATH: $env:PATH += ';C:\\Program Files\\Graphviz\\bin'")
            print("3. Or restart your terminal after installation")
        elif platform.system() == "Darwin":  # macOS
            print("1. Install with Homebrew: brew install graphviz")
        else:  # Linux
            print("1. Ubuntu/Debian: sudo apt-get install graphviz")
            print("2. RHEL/CentOS: sudo yum install graphviz")
            
        print(f"\n🔧 Error details: {e}")
        return False
    
    print("✅ Graphviz is working! Generating workflow diagram...")
    
    dot = Digraph('MCP_Agent_Architecture', comment='MCP Web Scraping Agent Architecture')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.2')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Helvetica')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # User Interface Layer
    with dot.subgraph(name='cluster_users') as c:
        c.attr(style='filled', color='lightgrey', label='User Interfaces')
        c.node('web_user', 'Web Users\n(Browser/API)', shape='ellipse', fillcolor='beige')
        c.node('mcp_user', 'AI Applications\n(Claude, VS Code)', shape='ellipse', fillcolor='lightcyan')

    # Application Layer
    with dot.subgraph(name='cluster_app') as c:
        c.attr(style='filled', color='lightgreen', label='Unified FastAPI Application (main.py)')
        c.node('rest_api', 'REST Endpoints\n/scrape/, /data/, /agent/query/')
        c.node('mcp_api', 'MCP Endpoints\n/mcp/tools/, /mcp/call_tool/')
        c.node('router', 'Request Router\n& Validator', shape='diamond', fillcolor='orange')

    # Core Logic Layer
    with dot.subgraph(name='cluster_logic') as c:
        c.attr(style='filled', color='lightyellow', label='Core Logic & Services')
        c.node('agent_logic', 'Agent Logic\n(Memory Check & Flow)')
        c.node('llm_service', 'LLM Service\n(llm_service.py)', fillcolor='gold')
        c.node('scraper_logic', 'Scraping Logic\n(BeautifulSoup + Requests)')

    # Data & External Layer
    with dot.subgraph(name='cluster_data') as c:
        c.attr(style='filled', color='lightcoral', label='Data & External Services')
        c.node('database', 'SQLite Database\n(Agent Memory)', shape='cylinder', fillcolor='lightgreen')
        c.node('gemini', 'Google Gemini\n(AI Intelligence)', shape='diamond', fillcolor='gold')
        c.node('websites', 'Target Websites\n(URLs to Scrape)', shape='ellipse', fillcolor='lightpink')

    # Define main workflow edges
    dot.edge('web_user', 'rest_api', label='HTTP Requests')
    dot.edge('mcp_user', 'mcp_api', label='MCP Tool Calls')
    
    dot.edge('rest_api', 'router', label='Route')
    dot.edge('mcp_api', 'router', label='Route')
    
    dot.edge('router', 'agent_logic', label='Process Request')
    
    # Memory check flow
    dot.edge('agent_logic', 'database', label='Check Memory')
    dot.edge('database', 'agent_logic', label='Content Found/Not Found', style='dashed')
    
    # Scraping flow (when content not in memory)
    dot.edge('agent_logic', 'scraper_logic', label='Scrape if Needed', color='red')
    dot.edge('scraper_logic', 'websites', label='Fetch Content')
    dot.edge('websites', 'scraper_logic', label='HTML Content')
    dot.edge('scraper_logic', 'database', label='Store Content')
    
    # AI analysis flow
    dot.edge('agent_logic', 'llm_service', label='Send Context + Prompt')
    dot.edge('llm_service', 'gemini', label='API Call')
    dot.edge('gemini', 'llm_service', label='AI Response')
    dot.edge('llm_service', 'agent_logic', label='Processed Response')
    
    # Response flow
    dot.edge('agent_logic', 'router', label='Formatted Response')
    dot.edge('router', 'rest_api', label='JSON Response')
    dot.edge('router', 'mcp_api', label='Tool Response')
    
    dot.edge('rest_api', 'web_user', label='HTTP Response')
    dot.edge('mcp_api', 'mcp_user', label='MCP Result')

    # Render the diagram
    try:
        dot.render('assets/agent_workflow_diagram', format='png', view=True)
        print("🎨 Updated workflow diagram 'agent_workflow_diagram.png' has been generated!")
        print("📂 Saved to assets/ directory with new MCP architecture components.")
        return True
    except Exception as e:
        print(f"❌ Failed to render diagram: {e}")
        print("💡 The diagram source was generated successfully, but rendering failed.")
        print("📄 Check the .dot file for the raw Graphviz source.")
        return False

if __name__ == "__main__":
    create_workflow_diagram()