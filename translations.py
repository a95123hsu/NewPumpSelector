"""
Translation dictionaries for the Pump Selection Tool.
"""

TRANSLATIONS = {
    "English": {
        # App title and headers
        "Hung Pump": "Hung Pump",
        "Pump Selection Tool": "Pump Selection Tool",
        "Data loaded": "Data loaded: {n_records} records | Last update: {timestamp}",
        
        # Buttons
        "Refresh Data": "🔄 Refresh Data",
        "Reset Inputs": "🔄 Reset Inputs",
        "Search": "🔍 Search",
        "Show Curve": "📈 Show Pump Curve",
        "Update Curves": "📈 Update Curves",
        
        # Step 1
        "Step 1": "### 🔧 Step 1: Select Basic Criteria",
        "Category": "* Category:",
        "Frequency": "* Frequency (Hz):",
        "Phase": "* Phase:",
        "Select...": "Select...",
        "All Categories": "All Categories",
        "Show All Frequency": "Show All Frequency",
        "Show All Phase": "Show All Phase",
        
        # Column Selection
        "Column Selection": "📋 Column Selection",
        "Select Columns": "Select columns to display in results:",
        "Select All": "Select All",
        "Deselect All": "Deselect All",
        "Essential Columns": "Essential Columns (always shown)",
        
        # Categories
        "Dirty Water": "Dirty Water",
        "Clean Water": "Clean Water",
        "Speciality Pump": "Speciality Pump",
        "Grinder": "Grinder",
        "Construction": "Construction",
        "Sewage and Wastewater": "Sewage and Wastewater",
        "High Pressure": "High Pressure",
        "Booster": "Booster",
        "BLDC": "BLDC",
        
        # Application section
        "Application Input": "### 🏢 Application Input",
        "Floor Faucet Info": "💡 Each floor = 3.5 m TDH | Each faucet = 15 LPM",
        "Number of Floors": "Number of Floors",
        "Number of Faucets": "Number of Faucets",
        
        # Pond drainage
        "Pond Drainage": "### 🌊 Pond Drainage",
        "Pond Length": "Pond Length (m)",
        "Pond Width": "Pond Width (m)",
        "Pond Height": "Pond Height (m)",
        "Drain Time": "Drain Time (hours)",
        "Pond Volume": "📏 Pond Volume: {volume} L",
        "Required Flow": "💧 Required Flow to drain pond: {flow} LPM",
        
        # Underground
        "Pump Depth": "Pump Depth Below Ground (m)",
        "Particle Size": "Max Particle Size (mm)",
        
        # Manual Input
        "Manual Input": "### Manual Input",
        "Flow Unit": "Flow Unit",
        "Flow Value": "Flow Value",
        "Head Unit": "Head Unit",
        "TDH": "Total Dynamic Head (TDH)",
        
        # Estimated application
        "Estimated Application": "### 💡 Estimated Application (based on Manual Input)",
        "Estimated Floors": "Estimated Floors",
        "Estimated Faucets": "Estimated Faucets",
        
        # Results
        "Result Display": "### 📊 Result Display Control",
        "Show Percentage": "Show Top Percentage of Results",
        "Matching Pumps": "✅ Matching Pumps",
        "Found Pumps": "Found {count} matching pumps",
        "Matching Results": "### Matching Pumps Results",
        "Showing Results": "Showing all {count} results",
        "View Product": "View Product",
        "Select Pumps": "Select pumps from the table below to view their performance curves",
        
        # Pump Curve Section
        "Pump Curves": "### 📈 Pump Performance Curves",
        "Select Pump": "Select a pump to view its performance curve:",
        "No Curve Data": "No curve data available for this pump model",
        "Curve Data Loaded": "Curve data loaded: {count} pumps with curve data",
        "Performance Curve": "Performance Curve - {model}",
        "Flow Rate": "Flow Rate (LPM)",
        "Head": "Head (M)",
        "Operating Point": "Your Operating Point",
        "Efficiency Curve": "Efficiency Curve - {model}",
        "Efficiency": "Efficiency (%)",
        "Power Curve": "Power Curve - {model}",
        "Power": "Power (kW)",
        "Multiple Curves": "Performance Comparison",
        "Compare Pumps": "Compare Selected Pumps",
        "Select Multiple": "Select multiple pumps to compare:",
        "Select Pumps for Curves": "Select pumps to display their performance curves:",
        "Charts Update Info": "👆 Please select one or more pumps above and click 'Update Curves' to view their performance curves",
        "Loading Curve": "Loading curve data...",
        "Loading Comparison": "Loading comparison chart...",
        "Update Curves": "📈 Update Curves",
        "Selected Pumps": "Selected {count} pump(s) for curve visualization",
        
        # Column headers
        "Q Rated/LPM": "Q Rated/LPM",
        "Rated flow rate in liters per minute": "Rated flow rate in liters per minute",
        "Head Rated/M": "Head Rated/M",
        "Rated head in meters": "Rated head in meters",
        
        # Flow units
        "L/min": "L/min",
        "L/sec": "L/sec",
        "m³/hr": "m³/hr",
        "m³/min": "m³/min",
        "US gpm": "US gpm",
        
        # Head units
        "m": "m",
        "ft": "ft",
        
        # Warnings & Errors
        "Select Warning": "Please select Frequency and Phase to proceed.",
        "No Matches": "⚠️ No pumps match your criteria. Try adjusting the parameters.",
        "Failed Connection": "❌ Failed to connect to Supabase: {error}",
        "Failed Data": "❌ Failed to load data from Supabase: {error}",
        "Failed CSV": "❌ Failed to load CSV file: {error}",
        "No Data": "❌ No pump data available. Please check your Supabase connection or CSV file.",
        "Failed Curve Data": "❌ Failed to load curve data: {error}"
    },
    "繁體中文": {
        # App title and headers
        "Hung Pump": "宏泵集團",
        "Pump Selection Tool": "水泵選型工具",
        "Data loaded": "已載入資料: {n_records} 筆記錄 | 最後更新: {timestamp}",
        
        # Buttons
        "Refresh Data": "🔄 刷新資料",
        "Reset Inputs": "🔄 重置輸入",
        "Search": "🔍 搜尋",
        "Show Curve": "📈 顯示泵浦曲線",
        "Update Curves": "📈 更新曲線",
        
        # Step 1
        "Step 1": "### 🔧 步驟一: 選擇基本條件",
        "Category": "* 類別:",
        "Frequency": "* 頻率 (赫茲):",
        "Phase": "* 相數:",
        "Select...": "請選擇...",
        "All Categories": "所有類別",
        "Show All Frequency": "顯示所有頻率",
        "Show All Phase": "顯示所有相數",
        
        # Column Selection
        "Column Selection": "📋 欄位選擇",
        "Select Columns": "選擇要在結果中顯示的欄位:",
        "Select All": "全選",
        "Deselect All": "全部取消",
        "Essential Columns": "必要欄位 (總是顯示)",
        
        # Categories
        "Dirty Water": "污水泵",
        "Clean Water": "清水泵",
        "Speciality Pump": "特殊用途泵",
        "Grinder": "研磨泵",
        "Construction": "工業泵",
        "Sewage and Wastewater": "污水和廢水泵",
        "High Pressure": "高壓泵",
        "Booster": "加壓泵",
        "BLDC": "無刷直流泵",
        
        # Application section
        "Application Input": "### 🏢 應用輸入",
        "Floor Faucet Info": "💡 每樓層 = 3.5 米揚程 | 每水龍頭 = 15 LPM",
        "Number of Floors": "樓層數量",
        "Number of Faucets": "水龍頭數量",
        
        # Pond drainage
        "Pond Drainage": "### 🌊 池塘排水",
        "Pond Length": "池塘長度 (米)",
        "Pond Width": "池塘寬度 (米)",
        "Pond Height": "池塘高度 (米)",
        "Drain Time": "排水時間 (小時)",
        "Pond Volume": "📏 池塘體積: {volume} 升",
        "Required Flow": "💧 所需排水流量: {flow} LPM",
        
        # Underground
        "Pump Depth": "幫浦地下深度 (米)",
        "Particle Size": "最大固體顆粒尺寸 (毫米)",
        
        # Manual Input
        "Manual Input": "### 手動輸入",
        "Flow Unit": "流量單位",
        "Flow Value": "流量值",
        "Head Unit": "揚程單位",
        "TDH": "總動態揚程 (TDH)",
        
        # Estimated application
        "Estimated Application": "### 💡 估計應用 (基於手動輸入)",
        "Estimated Floors": "估計樓層",
        "Estimated Faucets": "估計水龍頭",
        
        # Results
        "Result Display": "### 📊 結果顯示控制",
        "Show Percentage": "顯示前百分比的結果",
        "Matching Pumps": "✅ 符合條件的幫浦",
        "Found Pumps": "找到 {count} 個符合的幫浦",
        "Matching Results": "### 符合幫浦結果",
        "Showing Results": "顯示全部 {count} 筆結果",
        "View Product": "查看產品",
        "Select Pumps": "從下表選擇幫浦以查看其性能曲線",
        
        # Pump Curve Section
        "Pump Curves": "### 📈 幫浦性能曲線",
        "Select Pump": "選擇幫浦以查看其性能曲線:",
        "No Curve Data": "此幫浦型號無曲線資料",
        "Curve Data Loaded": "曲線資料已載入: {count} 個幫浦有曲線資料",
        "Performance Curve": "性能曲線 - {model}",
        "Flow Rate": "流量 (LPM)",
        "Head": "揚程 (M)",
        "Operating Point": "您的操作點",
        "Efficiency Curve": "效率曲線 - {model}",
        "Efficiency": "效率 (%)",
        "Power Curve": "功率曲線 - {model}",
        "Power": "功率 (kW)",
        "Multiple Curves": "性能比較",
        "Compare Pumps": "比較選定的幫浦",
        "Select Multiple": "選擇多個幫浦進行比較:",
        "Select Pumps for Curves": "選擇幫浦以顯示其性能曲線:",
        "Charts Update Info": "👆 請在上方選擇一個或多個幫浦並點擊「更新曲線」以查看其性能曲線",
        "Loading Curve": "載入曲線資料中...",
        "Loading Comparison": "載入比較圖表中...",
        "Update Curves": "📈 更新曲線",
        "Selected Pumps": "已選擇 {count} 個幫浦進行曲線視覺化",
        
        # Column headers
        "Q Rated/LPM": "額定流量 (LPM)",
        "Rated flow rate in liters per minute": "每分鐘額定流量（公升）",
        "Head Rated/M": "額定揚程 (M)",
        "Rated head in meters": "額定揚程（米）",
        
        # Flow units
        "L/min": "公升/分鐘",
        "L/sec": "公升/秒",
        "m³/hr": "立方米/小時",
        "m³/min": "立方米/分鐘",
        "US gpm": "美制加侖/分鐘",
        
        # Head units
        "m": "米",
        "ft": "英尺",
        
        # Warnings & Errors
        "Select Warning": "請選擇頻率和相數以繼續。",
        "No Matches": "⚠️ 沒有符合您條件的幫浦。請調整參數。",
        "Failed Connection": "❌ 連接到 Supabase 失敗: {error}",
        "Failed Data": "❌ 從 Supabase 載入資料失敗: {error}",
        "Failed CSV": "❌ 載入 CSV 檔案失敗: {error}",
        "No Data": "❌ 無可用幫浦資料。請檢查您的 Supabase 連接或 CSV 檔案。",
        "Failed Curve Data": "❌ 載入曲線資料失敗: {error}"
    }
}

def get_text(key: str, **kwargs) -> str:
    """
    Get translated text for a given key.
    
    Args:
        key (str): The translation key
        **kwargs: Format parameters for the translation string
    
    Returns:
        str: The translated text
    """
    from streamlit import session_state
    
    # Get current language from session state
    current_lang = session_state.get('language', 'English')
    
    # Get translation dictionary for current language
    translations = TRANSLATIONS.get(current_lang, TRANSLATIONS['English'])
    
    # Get translation for key
    text = translations.get(key, key)
    
    # Format the text with any provided parameters
    return text.format(**kwargs) if kwargs else text 