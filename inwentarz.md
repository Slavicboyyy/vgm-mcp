# Inwentarz: co te projekty mają w kodzie

> Wyciągnięte z kodu 13 sklonowanych repozytoriów, nie z plików README.
> Narzędzi łącznie: 598. Osobnych nazw: 246.

Opisy w README bywają niepełne albo wymieniają narzędzia, których w kodzie nie ma.
Ta lista powstała przez odczytanie miejsc, w których serwery rejestrują narzędzia.

## Narzędzia powtarzające się w kilku projektach

Im więcej projektów ma dane narzędzie, tym pewniej jest potrzebne.

| narzędzie | w ilu projektach | opis |
|---|---:|---|
| `chart_get_state` | 6 | Read the current chart state: symbol, timeframe, visible studies, and last price. |
| `chart_set_symbol` | 6 | Change the active chart symbol (e.g. |
| `chart_set_timeframe` | 6 | Change the active chart timeframe / resolution. |
| `pine_compile` | 6 | Compile the current Pine Script and add it to the chart. WARNING: this SAVES first, clicking Save an |
| `pine_get_source` | 6 | Read the current Pine Editor source code. Pine Editor must be open. |
| `pine_save` | 6 | Save the current Pine Script buffer to the saved script the editor is bound to. WARNING: this persis |
| `pine_set_source` | 6 | Set Pine Script source code in the editor. Refuses to overwrite a buffer holding real content unless |
| `quote_get` | 6 | Get real-time quote data for a symbol (price, OHLC, volume). If symbol is provided and differs from  |
| `alert_create` | 5 | Create a price alert on the current chart symbol via TradingView\ |
| `alert_delete` | 5 | Delete all alerts or open context menu for deletion |
| `alert_list` | 5 | List active alerts |
| `batch_run` | 5 | Run an action across multiple symbols and/or timeframes |
| `capture_screenshot` | 5 | Take a screenshot of the TradingView chart |
| `chart_get_visible_range` | 5 | Get the visible date range (unix timestamps) and bars range on the chart |
| `chart_manage_indicator` | 5 | Add or remove an indicator/study on the chart |
| `chart_scroll_to_date` | 5 | Jump the chart view to center on a specific date |
| `chart_set_type` | 5 | Change chart type |
| `chart_set_visible_range` | 5 | Zoom the chart to a specific date range (unix timestamps) |
| `data_get_equity` | 5 | Get equity curve data from Strategy Tester. Pass entity_id when more than one strategy is loaded. |
| `data_get_indicator` | 5 | Get indicator/study info and input values |
| `data_get_ohlcv` | 5 | Get OHLCV bar data from the chart. Use summary=true for compact stats instead of all bars (saves con |
| `data_get_pine_boxes` | 5 | Read box/zone boundaries drawn by Pine Script indicators (box.new). Returns deduplicated {high, low} |
| `data_get_pine_labels` | 5 | Read text labels drawn by Pine Script indicators (label.new). Returns text and price pairs. Use stud |
| `data_get_pine_lines` | 5 | Read horizontal price levels drawn by Pine Script indicators (line.new). Returns deduplicated price  |
| `data_get_pine_tables` | 5 | Read table data drawn by Pine Script indicators (table.new). Returns formatted text rows per table.  |
| `data_get_strategy_results` | 5 | Get strategy performance metrics from Strategy Tester. Auto-opens the panel and auto-unhides a hidde |
| `data_get_study_values` | 5 | Get current indicator values from the data window for all visible studies (RSI, MACD, Bollinger Band |
| `data_get_trades` | 5 | Get the most recent strategy orders. Pass entity_id when more than one strategy is loaded. Auto-open |
| `depth_get` | 5 | Get order book / DOM (Depth of Market) data from the chart |
| `draw_clear` | 5 | Remove ALL drawings from the ACTIVE PANE. On a multi-pane layout this is NOT the whole chart: use pa |
| `draw_get_properties` | 5 | Get properties and points of a specific drawing |
| `draw_list` | 5 | List shapes/drawings on the ACTIVE PANE ONLY. On a multi-pane layout the other panes are not include |
| `draw_remove_one` | 5 | Remove a specific drawing by entity ID |
| `draw_shape` | 5 | Draw a shape/line on the chart |
| `indicator_set_inputs` | 5 | Change indicator/study input values (e.g., length, source, period) |
| `indicator_toggle_visibility` | 5 | Show, hide, or flip an indicator on the chart. Omit visible to toggle. Confirms the result by readin |
| `layout_list` | 5 | List saved chart layouts with bounded pagination |
| `layout_switch` | 5 | Switch to a saved chart layout by name or ID. Stops rather than discarding unsaved changes on the cu |
| `pane_focus` | 5 | Focus a specific chart pane by index (0-based) |
| `pane_list` | 5 | List all chart panes in the current layout with their symbols and active state |
| `pane_set_layout` | 5 | Change the chart grid layout (e.g., single, 2x2, 2h, 3v) |
| `pane_set_symbol` | 5 | Set the symbol on a specific pane by index |
| `pine_analyze` | 5 | Run static analysis on Pine Script code WITHOUT compiling — catches array out-of-bounds, unguarded a |
| `pine_check` | 5 | Compile Pine Script via TradingView\ |
| `pine_get_console` | 5 | Read Pine Script console/log output (compile messages, log.info(), errors) |
| `pine_get_errors` | 5 | Get Pine Script compilation errors from Monaco markers |
| `pine_list_scripts` | 5 | List saved Pine Scripts. Returns a page, not the whole library — pass name_filter to find one by nam |
| `pine_new` | 5 | Replace the Pine editor buffer with a blank template. WARNING: this does NOT create a new saved scri |
| `pine_open` | 5 | Open a saved Pine Script by name |
| `pine_smart_compile` | 5 | Intelligent compile: detects button, compiles, checks errors, reports study changes WARNING: like pi |
| `replay_autoplay` | 5 | Turn autoplay on or off in replay mode, optionally setting the speed. Pass enabled to say which stat |
| `replay_start` | 5 | Start bar replay mode, optionally at a specific date |
| `replay_status` | 5 | Get current replay mode status |
| `replay_step` | 5 | Advance one bar in replay mode |
| `replay_stop` | 5 | Stop replay and return to realtime |
| `replay_trade` | 5 | Execute a trade action in replay mode (buy, sell, or close position) |
| `symbol_info` | 5 | Get detailed metadata about the current symbol (name, exchange, type, description) |
| `symbol_search` | 5 | Search for symbols by name or keyword |
| `tab_close` | 5 | Close the currently active chart tab. Names the tab it is about to close and refuses when no tab is  |
| `tab_list` | 5 | List all open TradingView chart tabs |
| `tab_new` | 5 | Open a new chart tab. Optionally pick what to load in it: layout |
| `tab_switch` | 5 | Switch to a chart tab by index |
| `tv_discover` | 5 | Report which known TradingView API paths are available and their methods |
| `tv_health_check` | 5 | Check CDP, TradingView market-data connection, compatibility, and current chart state |
| `tv_launch` | 5 | Launch TradingView Desktop with Chrome DevTools Protocol (remote debugging) enabled. Auto-detects in |
| `tv_ui_state` | 5 | Get current UI state: which panels are open, what buttons are visible/enabled/disabled |
| `ui_click` | 5 | Click a UI element by aria-label, data-name, text content, or class substring |
| `ui_evaluate` | 5 | Execute JavaScript code in the TradingView page context for advanced automation. GATED: requires TV_ |
| `ui_find_element` | 5 | Find UI elements by text, aria-label, or CSS selector and return their positions |
| `ui_fullscreen` | 5 | Toggle TradingView fullscreen mode |
| `ui_hover` | 5 | Hover over a UI element by aria-label, data-name, or text content |
| `ui_keyboard` | 5 | Press keyboard keys or shortcuts (e.g., Enter, Escape, Alt+S, Ctrl+Z) |
| `ui_mouse_click` | 5 | Click at specific x,y coordinates on the TradingView window |
| `ui_open_panel` | 5 | Open, close, or toggle TradingView panels (pine-editor, strategy-tester, watchlist, alerts, trading) |
| `ui_scroll` | 5 | Scroll the chart or page up/down/left/right |
| `ui_type_text` | 5 | Type text into the currently focused input/textarea element. Refuses when nothing is focused or the  |
| `watchlist_add` | 5 | Add a symbol to the TradingView watchlist |
| `watchlist_get` | 5 | Get every symbol in the active TradingView watchlist. Membership comes from the symbols_list API so  |

## Wszystkie narzędzia, projekt po projekcie


### `FerroxLabs/tvcontrol` — 113 narzędzi

`alert_create`, `alert_create_bulk`, `alert_delete`, `alert_delete_by_id`, `alert_list`, `batch_run`, `capture_screenshot`, `chart_get_state`, `chart_get_visible_range`, `chart_manage_indicator`, `chart_scroll_to_date`, `chart_set_symbol`, `chart_set_timeframe`, `chart_set_type`, `chart_set_visible_range`, `chart_vision_read`, `data_get_equity`, `data_get_indicator`, `data_get_ohlcv`, `data_get_pine_boxes`, `data_get_pine_labels`, `data_get_pine_lines`, `data_get_pine_tables`, `data_get_strategy_results`, `data_get_study_values`, `data_get_trades`, `depth_get`, `draw_clear`, `draw_get_properties`, `draw_list`, `draw_remove_one`, `draw_shape`, `indicator_add_from_search`, `indicator_get_inputs`, `indicator_search`, `indicator_set_inputs`, `indicator_toggle_visibility`, `layout_create`, `layout_get_active`, `layout_list`, `layout_save`, `layout_switch`, `pane_focus`, `pane_list`, `pane_set_layout`, `pane_set_symbol`, `pine_analyze`, `pine_check`, `pine_compile`, `pine_get_console`, `pine_get_errors`, `pine_get_source`, `pine_list_scripts`, `pine_new`, `pine_open`, `pine_save`, `pine_set_source`, `pine_smart_compile`, `quote_batch`, `quote_get`, `replay_autoplay`, `replay_start`, `replay_status`, `replay_step`, `replay_stop`, `replay_trade`, `state_delete`, `state_list`, `state_restore`, `state_snapshot`, `strategy_sweep`, `symbol_info`, `symbol_search`, `tab_close`, `tab_list`, `tab_new`, `tab_switch`, `tv_capability_matrix`, `tv_chart_health`, `tv_compatibility_check`, `tv_compatibility_snapshot`, `tv_discover`, `tv_health_check`, `tv_launch`, `tv_repair_chart`, `tv_support_bundle`, `tv_ui_state`, `tv_update`, `tv_watchdog_history`, `tv_watchdog_sample`, `tv_watchdog_start`, `tv_watchdog_status`, `tv_watchdog_stop`, `ui_click`, `ui_evaluate`, `ui_find_element`, `ui_fullscreen`, `ui_hover`, `ui_keyboard`, `ui_mouse_click`, `ui_open_panel`, `ui_scroll`, `ui_type_text`, `watchlist_add`, `watchlist_add_bulk`, `watchlist_create`, `watchlist_export`, `watchlist_get`, `watchlist_get_by_id`, `watchlist_import`, `watchlist_list`, `watchlist_remove`, `watchlist_remove_bulk`

### `Spoofkapoof/TradingViewMCPServer` — 33 narzędzi

`analyze_pair`, `autocomplete_pine`, `calculate_correlation`, `convert_pine_version`, `detect_pine_version`, `detect_unfilled_gaps`, `explain_pine_error`, `get_adx`, `get_atr`, `get_bollinger_bands`, `get_cci`, `get_fibonacci_retracement`, `get_ichimoku_cloud`, `get_macd`, `get_market_profile`, `get_moving_averages`, `get_multiple_prices`, `get_pine_documentation`, `get_pine_template`, `get_pivot_points`, `get_price`, `get_rsi`, `get_server_stats`, `get_stochastic`, `get_support_resistance`, `get_volume_profile`, `get_vwap`, `get_williams_r`, `health_check`, `list_available_pairs`, `list_supported_assets`, `test_pine_script`, `validate_pine_script`

### `Weebapp003/tradingview-mcp` — 78 narzędzi

`alert_create`, `alert_delete`, `alert_list`, `batch_run`, `capture_screenshot`, `chart_get_state`, `chart_get_visible_range`, `chart_manage_indicator`, `chart_scroll_to_date`, `chart_set_symbol`, `chart_set_timeframe`, `chart_set_type`, `chart_set_visible_range`, `data_get_equity`, `data_get_indicator`, `data_get_ohlcv`, `data_get_pine_boxes`, `data_get_pine_labels`, `data_get_pine_lines`, `data_get_pine_tables`, `data_get_strategy_results`, `data_get_study_values`, `data_get_trades`, `depth_get`, `draw_clear`, `draw_get_properties`, `draw_list`, `draw_remove_one`, `draw_shape`, `indicator_set_inputs`, `indicator_toggle_visibility`, `layout_list`, `layout_switch`, `pane_focus`, `pane_list`, `pane_set_layout`, `pane_set_symbol`, `pine_analyze`, `pine_check`, `pine_compile`, `pine_get_console`, `pine_get_errors`, `pine_get_source`, `pine_list_scripts`, `pine_new`, `pine_open`, `pine_save`, `pine_set_source`, `pine_smart_compile`, `quote_get`, `replay_autoplay`, `replay_start`, `replay_status`, `replay_step`, `replay_stop`, `replay_trade`, `symbol_info`, `symbol_search`, `tab_close`, `tab_list`, `tab_new`, `tab_switch`, `tv_discover`, `tv_health_check`, `tv_launch`, `tv_ui_state`, `ui_click`, `ui_evaluate`, `ui_find_element`, `ui_fullscreen`, `ui_hover`, `ui_keyboard`, `ui_mouse_click`, `ui_open_panel`, `ui_scroll`, `ui_type_text`, `watchlist_add`, `watchlist_get`

### `atilaahmettaner/tradingview-mcp` — 39 narzędzi

`advanced_candle_pattern`, `backtest_strategy`, `bitcoin_market_pulse`, `bollinger_scan`, `coin_analysis`, `combined_analysis`, `compare_strategies`, `consecutive_candles_scan`, `egx_fibonacci_retracement`, `egx_index_analysis`, `egx_market_overview`, `egx_sector_scan`, `egx_sector_scanner`, `egx_smart_money_scanner`, `egx_stock_screener`, `egx_trade_plan`, `financial_news`, `futures_category_snapshot`, `futures_market_overview`, `futures_top_movers`, `futures_watchlist`, `market_sentiment`, `market_snapshot`, `multi_agent_analysis`, `multi_timeframe_analysis`, `rating_filter`, `smart_money_analysis`, `smart_volume_scanner`, `stock_extended_hours`, `stock_options_chain`, `stock_options_unusual_activity`, `stock_prices`, `stock_screener`, `top_gainers`, `top_losers`, `volume_breakout_scanner`, `volume_confirmation_analysis`, `walk_forward_backtest_strategy`, `yahoo_price`

### `cklose2000/pinescript-mcp-server` — 23 narzędzi

`check_element_contains_text`, `check_element_visible`, `click_element`, `compare_pinescript_versions`, `convert_pinescript_version`, `fill_input`, `fix_pinescript_errors`, `format_pinescript`, `get_config_section`, `get_pinescript_config`, `get_pinescript_history`, `get_pinescript_template`, `navigate_to_url`, `reset_pinescript_config`, `save_pinescript_version`, `select_option`, `set_templates_directory`, `take_screenshot`, `test_connection`, `update_pinescript_config`, `upload_file`, `validate_pinescript`, `wait_for_navigation`

### `coocolab/Coocolab-Tradingview-MCP` — 81 narzędzi

`alert_create`, `alert_delete`, `alert_list`, `batch_run`, `capture_screenshot`, `chart_get_state`, `chart_get_visible_range`, `chart_manage_indicator`, `chart_scroll_to_date`, `chart_set_symbol`, `chart_set_timeframe`, `chart_set_type`, `chart_set_visible_range`, `data_get_equity`, `data_get_indicator`, `data_get_ohlcv`, `data_get_pine_boxes`, `data_get_pine_labels`, `data_get_pine_lines`, `data_get_pine_tables`, `data_get_strategy_results`, `data_get_study_values`, `data_get_trades`, `depth_get`, `draw_clear`, `draw_get_properties`, `draw_list`, `draw_remove_one`, `draw_shape`, `indicator_set_inputs`, `indicator_toggle_visibility`, `layout_list`, `layout_switch`, `morning_brief`, `pane_focus`, `pane_list`, `pane_set_layout`, `pane_set_symbol`, `pine_analyze`, `pine_check`, `pine_compile`, `pine_get_console`, `pine_get_errors`, `pine_get_source`, `pine_list_scripts`, `pine_new`, `pine_open`, `pine_save`, `pine_set_source`, `pine_smart_compile`, `quote_get`, `replay_autoplay`, `replay_start`, `replay_status`, `replay_step`, `replay_stop`, `replay_trade`, `session_get`, `session_save`, `symbol_info`, `symbol_search`, `tab_close`, `tab_list`, `tab_new`, `tab_switch`, `tv_discover`, `tv_health_check`, `tv_launch`, `tv_ui_state`, `ui_click`, `ui_evaluate`, `ui_find_element`, `ui_fullscreen`, `ui_hover`, `ui_keyboard`, `ui_mouse_click`, `ui_open_panel`, `ui_scroll`, `ui_type_text`, `watchlist_add`, `watchlist_get`

### `deonmenezes/tradingviewmcp` — 78 narzędzi

`alert_create`, `alert_delete`, `alert_list`, `batch_run`, `capture_screenshot`, `chart_get_state`, `chart_get_visible_range`, `chart_manage_indicator`, `chart_scroll_to_date`, `chart_set_symbol`, `chart_set_timeframe`, `chart_set_type`, `chart_set_visible_range`, `data_get_equity`, `data_get_indicator`, `data_get_ohlcv`, `data_get_pine_boxes`, `data_get_pine_labels`, `data_get_pine_lines`, `data_get_pine_tables`, `data_get_strategy_results`, `data_get_study_values`, `data_get_trades`, `depth_get`, `draw_clear`, `draw_get_properties`, `draw_list`, `draw_remove_one`, `draw_shape`, `indicator_set_inputs`, `indicator_toggle_visibility`, `layout_list`, `layout_switch`, `pane_focus`, `pane_list`, `pane_set_layout`, `pane_set_symbol`, `pine_analyze`, `pine_check`, `pine_compile`, `pine_get_console`, `pine_get_errors`, `pine_get_source`, `pine_list_scripts`, `pine_new`, `pine_open`, `pine_save`, `pine_set_source`, `pine_smart_compile`, `quote_get`, `replay_autoplay`, `replay_start`, `replay_status`, `replay_step`, `replay_stop`, `replay_trade`, `symbol_info`, `symbol_search`, `tab_close`, `tab_list`, `tab_new`, `tab_switch`, `tv_discover`, `tv_health_check`, `tv_launch`, `tv_ui_state`, `ui_click`, `ui_evaluate`, `ui_find_element`, `ui_fullscreen`, `ui_hover`, `ui_keyboard`, `ui_mouse_click`, `ui_open_panel`, `ui_scroll`, `ui_type_text`, `watchlist_add`, `watchlist_get`

### `ertugrul59/tradingview-chart-mcp` — 2 narzędzi

`get_performance_stats`, `get_tradingview_chart_image`

### `fiale-plus/tradingview-mcp-server` — 12 narzędzi

`get_market_metainfo`, `get_preset`, `get_ta_summary`, `list_fields`, `list_presets`, `lookup_symbols`, `rank_by_ta`, `screen_crypto`, `screen_etf`, `screen_forex`, `screen_stocks`, `search_symbols`

### `jaipreet15/tradingview-mcp` — 28 narzędzi

`advanced_candle_pattern`, `backtest_strategy`, `bitcoin_market_pulse`, `bollinger_scan`, `coin_analysis`, `combined_analysis`, `compare_strategies`, `consecutive_candles_scan`, `financial_news`, `futures_category_snapshot`, `futures_market_overview`, `futures_top_movers`, `futures_watchlist`, `market_sentiment`, `market_snapshot`, `multi_agent_analysis`, `multi_timeframe_analysis`, `rating_filter`, `smart_volume_scanner`, `stock_extended_hours`, `stock_options_chain`, `stock_options_unusual_activity`, `top_gainers`, `top_losers`, `volume_breakout_scanner`, `volume_confirmation_analysis`, `walk_forward_backtest_strategy`, `yahoo_price`

### `moondevonyt/Trading-View-MCP-for-AI-by-Moon-Dev` — 16 narzędzi

`tv_add_indicator`, `tv_compile_pine_script`, `tv_get_backtest_results`, `tv_get_current_symbol`, `tv_list_indicators`, `tv_open_pine_editor`, `tv_read_indicator_value`, `tv_remove_all_indicators`, `tv_remove_indicator`, `tv_run_strategy_tester`, `tv_save_pine_script`, `tv_screenshot`, `tv_set_symbol`, `tv_set_timeframe`, `tv_validate_pine_script`, `tv_write_pine_script`

### `pueschel88/Tradingview-MCP` — 11 narzędzi

`chart_get_ohlcv`, `chart_get_state`, `chart_set_symbol`, `chart_set_timeframe`, `pine_compile`, `pine_get_source`, `pine_save`, `pine_set_source`, `quote_get`, `screenshot_chart`, `screenshot_full`

### `tradesdontlie/tradingview-mcp` — 84 narzędzi

`alert_create`, `alert_delete`, `alert_list`, `batch_run`, `capture_screenshot`, `chart_get_state`, `chart_get_visible_range`, `chart_manage_indicator`, `chart_scroll_to_date`, `chart_set_symbol`, `chart_set_timeframe`, `chart_set_type`, `chart_set_visible_range`, `data_get_equity`, `data_get_indicator`, `data_get_ohlcv`, `data_get_pine_boxes`, `data_get_pine_labels`, `data_get_pine_lines`, `data_get_pine_tables`, `data_get_strategy_results`, `data_get_study_values`, `data_get_trades`, `depth_get`, `draw_clear`, `draw_get_properties`, `draw_list`, `draw_remove_one`, `draw_shape`, `indicator_add`, `indicator_search`, `indicator_set_inputs`, `indicator_toggle_visibility`, `layout_list`, `layout_new`, `layout_switch`, `pane_focus`, `pane_list`, `pane_set_layout`, `pane_set_symbol`, `pine_analyze`, `pine_check`, `pine_compile`, `pine_get_console`, `pine_get_errors`, `pine_get_source`, `pine_list_scripts`, `pine_new`, `pine_open`, `pine_save`, `pine_set_source`, `pine_smart_compile`, `quote_get`, `replay_autoplay`, `replay_start`, `replay_status`, `replay_step`, `replay_stop`, `replay_trade`, `symbol_info`, `symbol_search`, `tab_close`, `tab_list`, `tab_new`, `tab_switch`, `tv_discover`, `tv_health_check`, `tv_launch`, `tv_ui_state`, `tv_update`, `ui_click`, `ui_evaluate`, `ui_find_element`, `ui_fullscreen`, `ui_hover`, `ui_keyboard`, `ui_mouse_click`, `ui_open_panel`, `ui_scroll`, `ui_type_text`, `watchlist_add`, `watchlist_add_bulk`, `watchlist_get`, `watchlist_remove`