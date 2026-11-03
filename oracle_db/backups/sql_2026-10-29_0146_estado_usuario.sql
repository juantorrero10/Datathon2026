prompt --application/set_environment
set define off verify off feedback off
whenever sqlerror exit sql.sqlcode rollback
--------------------------------------------------------------------------------
--
-- Oracle APEX export file
--
-- You should run this script using a SQL client connected to the database as
-- the owner (parsing schema) of the application or as a database user with the
-- APEX_ADMINISTRATOR_ROLE role.
--
-- This export file has been automatically generated. Modifying this file is not
-- supported by Oracle and can lead to unexpected application and/or instance
-- behavior now or in the future.
--
-- NOTE: Calls to apex_application_install override the defaults below.
--
--------------------------------------------------------------------------------
begin
wwv_flow_imp.import_begin (
 p_version_yyyy_mm_dd=>'2026.03.30'
,p_release=>'26.1.5'
,p_default_workspace_id=>9407325500210183
,p_default_application_id=>215
,p_default_id_offset=>10379708080259169
,p_default_owner=>'WKSP_DATATHON'
);
end;
/
 
prompt APPLICATION 215 - Pueblos con Vida
--
-- Application Export:
--   Application:     215
--   Name:            Pueblos con Vida
--   Exported By:     WKSP_DATATHON
--   Flashback:       0
--   Export Type:     Application Export
--     Pages:                      5
--       Processes:                6
--       Regions:                  5
--     Shared Components:
--       Logic:
--       Navigation:
--         Lists:                  2
--       Security:
--         Authentication:         1
--       User Interface:
--         Themes:                 1
--         Templates:
--       PWA:
--       Globalization:
--       Reports:
--       E-Mail:
--     Supporting Objects:  Included
--   Version:         26.1.5
--   Instance ID:     9389724618832531
--

prompt --application/delete_application
begin
wwv_flow_imp.remove_flow(wwv_flow.g_flow_id);
end;
/
prompt --application/create_application
begin
wwv_imp_workspace.create_flow(
 p_id=>wwv_flow.g_flow_id
,p_owner=>nvl(wwv_flow_application_install.get_schema,'WKSP_DATATHON')
,p_name=>nvl(wwv_flow_application_install.get_application_name,'Pueblos con Vida')
,p_alias=>nvl(wwv_flow_application_install.get_application_alias,'PUEBLOSVIDA215')
,p_page_view_logging=>'YES'
,p_page_protection_enabled_y_n=>'Y'
,p_checksum_salt=>'A1B2C3D4E5F6789012345678901234567890ABCDEF1234567890ABCDEF123456'
,p_bookmark_checksum_function=>'SH512'
,p_max_session_length_sec=>28800
,p_max_session_idle_sec=>3600
,p_compatibility_mode=>'24.2'
,p_flow_language=>'es'
,p_flow_language_derived_from=>'FLOW_PRIMARY_LANGUAGE'
,p_date_format=>'DD/MM/YYYY'
,p_timestamp_format=>'DD/MM/YYYY HH24:MI'
,p_timestamp_tz_format=>'DS'
,p_flow_image_prefix=>nvl(wwv_flow_application_install.get_image_prefix,'')
,p_authentication_id=>wwv_flow_imp.id(143622573347876321)
,p_application_tab_set=>0
,p_logo_type=>'T'
,p_logo_text=>'Pueblos con Vida'
,p_public_user=>'APEX_PUBLIC_USER'
,p_proxy_server=>nvl(wwv_flow_application_install.get_proxy,'')
,p_no_proxy_domains=>nvl(wwv_flow_application_install.get_no_proxy_domains,'')
,p_flow_version=>'24.2.0'
,p_flow_status=>'AVAILABLE_W_EDIT_LINK'
,p_browser_cache=>'N'
,p_browser_frame=>'S'
,p_deep_linking=>'Y'
,p_authorize_batch_job=>'N'
,p_rejoin_existing_sessions=>'N'
,p_csv_encoding=>'Y'
,p_modernization_available=>'Y'
,p_substitution_string_01=>'APP_NAME'
,p_substitution_value_01=>'Pueblos con Vida'
,p_file_prefix=>nvl(wwv_flow_application_install.get_static_app_file_prefix,'')
,p_files_version=>1
,p_version_scn=>'51016404140344'
,p_print_server_type=>'INSTANCE'
,p_file_storage=>'DB'
,p_is_pwa=>'N'
,p_theme_id=>42
,p_home_url=>'f?p=&APP_ID.:1:&APP_SESSION.::&DEBUG.:::'
,p_login_url=>'f?p=&APP_ID.:101:&APP_SESSION.::&DEBUG.:::'
,p_theme_style_by_user_pref=>false
,p_built_with_love=>false
,p_navigation_list_id=>wwv_flow_imp.id(143622573347876324)
,p_navigation_list_position=>'SIDE'
,p_navigation_list_template_id=>2469215554099805162
,p_nav_list_template_options=>'#DEFAULT#:js-defaultCollapsed:js-navCollapsed--hidden:t-TreeNav--styleA'
,p_nav_bar_type=>'LIST'
,p_nav_bar_list_id=>wwv_flow_imp.id(143622573347876325)
,p_nav_bar_list_template_id=>2849019392706229583
,p_nav_bar_template_options=>'#DEFAULT#'
);
end;
/
prompt --application/plugin_settings
begin
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144957505190972175)
,p_plugin_type=>'DYNAMIC ACTION'
,p_plugin=>'NATIVE_OPEN_AI_ASSISTANT'
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144957748384972176)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_COLOR_PICKER'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_as', 'POPUP',
  'mode', 'FULL')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144957883422972176)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_DATE_PICKER_APEX'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'appearance_behavior', 'MONTH-PICKER:YEAR-PICKER:TODAY-BUTTON',
  'days_outside_month', 'VISIBLE',
  'show_on', 'FOCUS',
  'time_increment', '15')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144957672660972176)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_GEOCODED_ADDRESS'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'background', 'default',
  'display_as', 'LIST',
  'map_preview', 'POPUP:ITEM',
  'match_mode', 'RELAX_HOUSE_NUMBER')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958213349972177)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_SELECT_MANY'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_values_as', 'separated')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144957553408972175)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_SINGLE_CHECKBOX'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'checked_value', 'Y',
  'unchecked_value', 'N')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144957957840972177)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_STAR_RATING'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'default_icon', 'fa-star',
  'tooltip', '#VALUE#')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958113790972177)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_YES_NO'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_style', 'SWITCH_CB',
  'off_value', 'N',
  'on_value', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958239682972178)
,p_plugin_type=>'PROCESS TYPE'
,p_plugin=>'NATIVE_GEOCODING'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'match_mode', 'RELAX_HOUSE_NUMBER')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958474442972178)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_DISPLAY_SELECTOR'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'include_slider', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958595501972179)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_IR'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'actions_menu_structure', 'IG')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958358785972178)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_MAP_REGION'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'use_vector_tile_layers', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958650973972179)
,p_plugin_type=>'WEB SOURCE TYPE'
,p_plugin=>'NATIVE_ADFBC'
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(144958806834972179)
,p_plugin_type=>'WEB SOURCE TYPE'
,p_plugin=>'NATIVE_BOSS'
);
end;
/
prompt --application/shared_components/navigation/lists/navigation_bar
begin
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(143622573347876325)
,p_name=>'Navigation Bar'
,p_static_id=>'navigation-bar'
,p_version_scn=>'1'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(143622573347876326)
,p_list_item_display_sequence=>10
,p_list_item_link_text=>'&APP_USER.'
,p_static_id=>'app-user'
,p_list_item_link_target=>'#'
,p_list_item_icon=>'fa-user'
,p_list_item_current_type=>'NEVER'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(143622573347876327)
,p_list_item_display_sequence=>20
,p_list_item_link_text=>'Logout'
,p_static_id=>'logout'
,p_list_item_link_target=>'&LOGOUT_URL.'
,p_list_item_icon=>'fa-sign-out'
,p_parent_list_item_id=>wwv_flow_imp.id(143622573347876326)
,p_list_item_current_type=>'NEVER'
);
end;
/
prompt --application/shared_components/navigation/lists/navigation_menu
begin
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(143622573347876324)
,p_name=>'Navigation Menu'
,p_static_id=>'navigation-menu'
,p_version_scn=>'1'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(143622573347876342)
,p_list_item_display_sequence=>40
,p_list_item_link_text=>'Datos'
,p_static_id=>'datos'
,p_list_item_link_target=>'f?p=&APP_ID.:30:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'TARGET_PAGE'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(143622573347876343)
,p_list_item_display_sequence=>30
,p_list_item_link_text=>'Mapa'
,p_static_id=>'mapa'
,p_list_item_link_target=>'f?p=&APP_ID.:40:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-map'
,p_list_item_current_type=>'TARGET_PAGE'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(143622573347876340)
,p_list_item_display_sequence=>20
,p_list_item_link_text=>'Simulador What-If'
,p_static_id=>'perfil-institucional'
,p_list_item_link_target=>'f?p=&APP_ID.:10:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-building'
,p_list_item_current_type=>'TARGET_PAGE'
);
end;
/
prompt --application/shared_components/navigation/listentry
begin
null;
end;
/
prompt --application/shared_components/navigation/navigation_bar
begin
null;
end;
/
prompt --application/shared_components/logic/application_settings
begin
null;
end;
/
prompt --application/shared_components/navigation/tabs/standard
begin
null;
end;
/
prompt --application/shared_components/navigation/tabs/parent
begin
null;
end;
/
prompt --application/pages/page_groups
begin
null;
end;
/
prompt --application/shared_components/navigation/breadcrumbentry
begin
null;
end;
/
prompt --application/shared_components/user_interface/themes
begin
wwv_flow_imp_shared.create_theme(
 p_id=>wwv_flow_imp.id(143622573347876323)
,p_theme_id=>42
,p_static_id=>'universal-theme'
,p_theme_name=>'Universal Theme'
,p_theme_internal_name=>'UNIVERSAL_THEME'
,p_version_identifier=>'26.1'
,p_navigation_type=>'L'
,p_nav_bar_type=>'LIST'
,p_is_locked=>false
,p_current_theme_style_id=>2722798454316704879
,p_default_page_template=>4073832297226169690
,p_default_dialog_template=>2101883943284197310
,p_error_template=>2102634289808461002
,p_printer_friendly_template=>4073832297226169690
,p_login_template=>2102634289808461002
,p_default_button_template=>4073839297780169708
,p_default_region_template=>4073835273271169698
,p_default_chart_template=>4073835273271169698
,p_default_form_template=>4073835273271169698
,p_default_reportr_template=>4073835273271169698
,p_default_wizard_template=>4073835273271169698
,p_default_menur_template=>2532939663579242476
,p_default_listr_template=>4073835273271169698
,p_default_irr_template=>2102002977963900996
,p_default_report_template=>2540130677583398057
,p_default_label_template=>1610598304472262251
,p_default_menu_template=>4073839682315169711
,p_default_list_template=>4073837480889169704
,p_default_top_nav_list_temp=>2528231041045349458
,p_default_side_nav_list_temp=>2469215554099805162
,p_default_nav_list_position=>'SIDE'
,p_default_dialogbtnr_template=>2127905476394690047
,p_default_dialogr_template=>4502917002193490937
,p_default_option_label=>1610598304472262251
,p_default_required_label=>1610598484065263269
,p_default_navbar_list_template=>2849019392706229583
,p_file_prefix=>nvl(wwv_flow_application_install.get_static_theme_file_prefix(42),'#APEX_FILES#themes/theme_42/26.1/')
,p_files_version=>64
,p_icon_library=>'FONTAPEX'
,p_javascript_file_urls=>wwv_flow_string.join(wwv_flow_t_varchar2(
'#APEX_FILES#libraries/apex/#MIN_DIRECTORY#widget.stickyWidget#MIN#.js?v=#APEX_VERSION#',
'#THEME_FILES#js/theme42#MIN#.js?v=#APEX_VERSION#'))
,p_css_file_urls=>'#THEME_FILES#css/Core#MIN#.css?v=#APEX_VERSION#'
,p_reference_id=>wwv_imp_util.get_subscription_id(4073840274158169736,2000,'universal-theme',8842.261)
,p_version_scn_master=>'SH256:WOPVC8vP1TPWUxczh2dJ4mCZcNGSTzA1cn8DjR2oQjY'
);
end;
/
prompt --application/shared_components/user_interface/theme_style
begin
null;
end;
/
prompt --application/shared_components/user_interface/theme_files
begin
null;
end;
/
prompt --application/shared_components/user_interface/template_opt_groups
begin
null;
end;
/
prompt --application/shared_components/user_interface/template_options
begin
null;
end;
/
prompt --application/shared_components/globalization/language
begin
null;
end;
/
prompt --application/shared_components/logic/build_options
begin
null;
end;
/
prompt --application/shared_components/globalization/messages
begin
null;
end;
/
prompt --application/shared_components/globalization/dyntranslations
begin
null;
end;
/
prompt --application/shared_components/security/authentications/app_authentication
begin
wwv_flow_imp_shared.create_authentication(
 p_id=>wwv_flow_imp.id(143622573347876321)
,p_name=>'App Authentication'
,p_static_id=>'app-authentication'
,p_scheme_type=>'NATIVE_APEX_ACCOUNTS'
,p_invalid_session_type=>'LOGIN'
,p_use_secure_cookie_yn=>'N'
,p_ras_mode=>0
,p_version_scn=>'1'
);
end;
/
prompt --application/user_interfaces/combined_files
begin
null;
end;
/
prompt --application/pages/page_00001
begin
wwv_flow_imp_page.create_page(
 p_id=>1
,p_name=>'Inicio'
,p_alias=>'INICIO'
,p_step_title=>'Inicio'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'13'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(143622573347876329)
,p_plug_name=>'Portada'
,p_static_id=>'portada'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN',
'  HTP.P(q''~<style>',
'.pv-portal {',
'  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;',
'  max-width: 1240px;',
'  margin: 0 auto;',
'  color: #0f172a;',
'  padding: 8px 16px 36px;',
'}',
'.pv-portal .hero {',
'  background: linear-gradient(135deg, #091e3a 0%, #112d4e 50%, #1a3e68 100%);',
'  color: #ffffff;',
'  border-radius: 20px;',
'  padding: 44px 44px 38px;',
'  margin: 8px 0 24px;',
'  box-shadow: 0 10px 30px -5px rgba(9, 30, 58, 0.35);',
'  position: relative;',
'  overflow: hidden;',
'  border: 1px solid rgba(255, 255, 255, 0.1);',
'}',
'.pv-portal .hero::after {',
'  content: "";',
'  position: absolute;',
'  top: -60px;',
'  right: -60px;',
'  width: 320px;',
'  height: 320px;',
'  background: radial-gradient(circle, rgba(16, 185, 129, 0.18) 0%, rgba(14, 165, 233, 0.08) 50%, transparent 70%);',
'  border-radius: 50%;',
'  pointer-events: none;',
'}',
'.pv-portal .top-badge-bar {',
'  display: flex;',
'  align-items: center;',
'  gap: 12px;',
'  margin-bottom: 16px;',
'  flex-wrap: wrap;',
'}',
'.pv-portal .kick {',
'  font-size: 11px;',
'  letter-spacing: 0.14em;',
'  text-transform: uppercase;',
'  color: #93c5fd;',
'  font-weight: 800;',
'  display: flex;',
'  align-items: center;',
'  gap: 6px;',
'}',
'.pv-portal .live-pill {',
'  background: rgba(16, 185, 129, 0.2);',
'  border: 1px solid #10b981;',
'  color: #34d399;',
'  font-size: 10px;',
'  font-weight: 800;',
'  letter-spacing: 0.08em;',
'  text-transform: uppercase;',
'  padding: 3px 10px;',
'  border-radius: 20px;',
'  display: inline-flex;',
'  align-items: center;',
'  gap: 6px;',
'}',
'.pv-portal .live-dot {',
'  width: 7px;',
'  height: 7px;',
'  background-color: #10b981;',
'  border-radius: 50%;',
'  box-shadow: 0 0 8px #10b981;',
'  animation: pv-pulse 2s infinite;',
'}',
'@keyframes pv-pulse {',
'  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }',
'  70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }',
'  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }',
'}',
'.pv-portal h1 {',
'  font-size: 40px;',
'  font-weight: 900;',
'  line-height: 1.1;',
'  margin: 0 0 12px;',
'  letter-spacing: -0.03em;',
'  color: #ffffff;',
'}',
'.pv-portal .sub {',
'  color: #cbd5e1;',
'  font-size: 16px;',
'  max-width: 860px;',
'  line-height: 1.55;',
'  margin: 0 0 28px;',
'  font-weight: 400;',
'}',
'.pv-portal .kpi-ribbon {',
'  display: grid;',
'  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));',
'  gap: 12px;',
'  background: rgba(255, 255, 255, 0.07);',
'  backdrop-filter: blur(8px);',
'  -webkit-backdrop-filter: blur(8px);',
'  border: 1px solid rgba(255, 255, 255, 0.12);',
'  border-radius: 14px;',
'  padding: 16px 20px;',
'}',
'.pv-portal .kpi-item { display: flex; flex-direction: column; }',
'.pv-portal .kpi-val {',
'  font-size: 24px;',
'  font-weight: 900;',
'  color: #38bdf8;',
'  letter-spacing: -0.02em;',
'  line-height: 1.1;',
'}',
'.pv-portal .kpi-lbl {',
'  font-size: 11px;',
'  text-transform: uppercase;',
'  letter-spacing: 0.06em;',
'  color: #94a3b8;',
'  font-weight: 600;',
'  margin-top: 4px;',
'}',
'.pv-portal .section-title {',
'  font-size: 13px;',
'  font-weight: 800;',
'  text-transform: uppercase;',
'  letter-spacing: 0.12em;',
'  color: #475569;',
'  margin: 28px 0 14px;',
'  display: flex;',
'  align-items: center;',
'  gap: 8px;',
'}',
'.pv-portal .cards-grid {',
'  display: grid;',
'  grid-template-columns: repeat(12, 1fr);',
'  gap: 18px;',
'}',
'.pv-portal .card {',
'  display: flex;',
'  flex-direction: column;',
'  text-decoration: none;',
'  color: inherit;',
'  background: #ffffff;',
'  border: 1px solid #e2e8f0;',
'  border-radius: 18px;',
'  padding: 24px;',
'  box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04), 0 8px 20px rgba(15, 23, 42, 0.05);',
'  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);',
'  position: relative;',
'  overflow: hidden;',
'}',
'.pv-portal .card:hover {',
'  transform: translateY(-4px);',
'  box-shadow: 0 16px 36px -6px rgba(15, 23, 42, 0.12);',
'  border-color: #cbd5e1;',
'}',
'.pv-portal .card:focus-visible {',
'  outline: 3px solid #38bdf8;',
'  outline-offset: 2px;',
'}',
'.pv-portal .card-span-7 { grid-column: span 7; }',
'.pv-portal .card-span-5 { grid-column: span 5; }',
'.pv-portal .card-span-6 { grid-column: span 6; }',
'.pv-portal .card-hero-accent { border-top: 4px solid #0284c7; }',
'.pv-portal .card-map-accent { border-top: 4px solid #10b981; }',
'.pv-portal .card-data-accent { border-top: 4px solid #8b5cf6; }',
'.pv-portal .card-tech-accent { border-top: 4px solid #f59e0b; }',
'.pv-portal .card-header {',
'  display: flex;',
'  justify-content: space-between;',
'  align-items: flex-start;',
'  margin-bottom: 14px;',
'  gap: 12px;',
'}',
'.pv-portal .badge {',
'  font-size: 10px;',
'  font-weight: 800;',
'  text-transform: uppercase;',
'  letter-spacing: 0.08em;',
'  padding: 4px 10px;',
'  border-radius: 6px;',
'  white-space: nowrap;',
'}',
'.pv-portal .badge-blue { background: #e0f2fe; color: #0369a1; }',
'.pv-portal .badge-green { background: #dcfce7; color: #15803d; }',
'.pv-portal .badge-purple { background: #f3e8ff; color: #7e22ce; }',
'.pv-portal .badge-amber { background: #fef3c7; color: #b45309; }',
'.pv-portal .ico-box {',
'  width: 44px;',
'  height: 44px;',
'  border-radius: 12px;',
'  display: flex;',
'  align-items: center;',
'  justify-content: center;',
'  flex: 0 0 auto;',
'}',
'.pv-portal .ico-box svg { width: 22px; height: 22px; }',
'.pv-portal .ico-blue { background: #e0f2fe; color: #0284c7; }',
'.pv-portal .ico-green { background: #dcfce7; color: #10b981; }',
'.pv-portal .ico-purple { background: #f3e8ff; color: #8b5cf6; }',
'.pv-portal .ico-amber { background: #fef3c7; color: #f59e0b; }',
'.pv-portal h2 {',
'  font-size: 20px;',
'  font-weight: 800;',
'  margin: 0 0 8px;',
'  color: #0f172a;',
'  letter-spacing: -0.01em;',
'}',
'.pv-portal p {',
'  font-size: 13.5px;',
'  color: #475569;',
'  line-height: 1.55;',
'  margin: 0 0 18px;',
'  flex-grow: 1;',
'}',
'.pv-portal .tags-row {',
'  display: flex;',
'  gap: 6px;',
'  flex-wrap: wrap;',
'  margin-bottom: 16px;',
'}',
'.pv-portal .tag {',
'  font-size: 11px;',
'  background: #f8fafc;',
'  border: 1px solid #e2e8f0;',
'  padding: 3px 8px;',
'  border-radius: 6px;',
'  color: #64748b;',
'  font-weight: 600;',
'}',
'.pv-portal .card-cta {',
'  font-size: 12.5px;',
'  font-weight: 800;',
'  display: flex;',
'  align-items: center;',
'  gap: 6px;',
'  transition: gap 0.15s ease;',
'  margin-top: auto;',
'}',
'.pv-portal .card:hover .card-cta { gap: 10px; }',
'.pv-portal .cta-blue { color: #0284c7; }',
'.pv-portal .cta-green { color: #059669; }',
'.pv-portal .cta-purple { color: #7c3aed; }',
'.pv-portal .cta-amber { color: #d97706; }',
'.pv-portal .footer {',
'  margin-top: 32px;',
'  padding-top: 20px;',
'  border-top: 1px solid #e2e8f0;',
'  display: flex;',
'  justify-content: space-between;',
'  align-items: center;',
'  flex-wrap: wrap;',
'  gap: 16px;',
'  font-size: 11.5px;',
'  color: #64748b;',
'}',
'.pv-portal .footer-sources { max-width: 780px; line-height: 1.5; }',
'.pv-portal .footer-badge {',
'  display: flex;',
'  align-items: center;',
'  gap: 8px;',
'  background: #f8fafc;',
'  border: 1px solid #e2e8f0;',
'  padding: 6px 12px;',
'  border-radius: 8px;',
'  font-weight: 700;',
'  color: #334155;',
'}',
'@media (max-width: 900px) {',
'  .pv-portal .card-span-7,',
'  .pv-portal .card-span-5,',
'  .pv-portal .card-span-6 { grid-column: span 12; }',
'  .pv-portal h1 { font-size: 30px; }',
'  .pv-portal .hero { padding: 28px 24px; }',
'  .pv-portal .footer { flex-direction: column; align-items: flex-start; }',
'}',
'</style>',
'',
'<div class="pv-portal">',
'  <div class="hero">',
'    <div class="top-badge-bar">',
'      <div class="kick">',
'        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
unistr('        II Datathon LoDCOREMadrid \00B7 2026'),
'      </div>',
'      <div class="live-pill">',
'        <span class="live-dot"></span>',
unistr('        Oracle AI 23ai \00B7 Modelos ONNX Activos'),
'      </div>',
'    </div>',
'',
'    <h1>Pueblos con Vida</h1>',
unistr('    <p class="sub">Plataforma de Inteligencia Territorial y Capacidad de Carga para la toma de decisiones en los 155 municipios de la Comunidad de Madrid con menos de 50.000 habitantes. Diagn\00F3stico din\00E1mico 2010\20132025, proyecciones a 2035 y simulaci\00F3n')
||unistr(' de pol\00EDticas p\00FAblicas sin sesgos.</p>'),
'',
'    <div class="kpi-ribbon">',
'      <div class="kpi-item"><span class="kpi-val">155</span><span class="kpi-lbl">Municipios (&lt; 50k hab.)</span></div>',
unistr('      <div class="kpi-item"><span class="kpi-val">2.480</span><span class="kpi-lbl">Observaciones Panel 2010\20132025</span></div>'),
'      <div class="kpi-item"><span class="kpi-val">6</span><span class="kpi-lbl">Modelos ONNX core in-DB</span></div>',
'      <div class="kpi-item"><span class="kpi-val">1,55%</span><span class="kpi-lbl">Error Backtest M3</span></div>',
'      <div class="kpi-item"><span class="kpi-val">&lt; 100 ms</span><span class="kpi-lbl">Tiempo de Inferencia</span></div>',
'    </div>',
'  </div>',
'',
'  <div class="section-title">',
'    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><re'
||'ct x="3" y="14" width="7" height="7"/></svg>',
unistr('    M\00F3dulos Estrat\00E9gicos de la Plataforma'),
'  </div>',
'',
'  <div class="cards-grid">',
'    <a class="card card-span-7 card-hero-accent" href="#" data-page="10">',
'      <div class="card-header">',
'        <div class="ico-box ico-blue">',
'          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="'
||'3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>',
'        </div>',
unistr('        <span class="badge badge-blue">Herramienta de Decisi\00F3n \00B7 P\00E1g. 10</span>'),
'      </div>',
'      <h2>Simulador What-If de Capacidad de Carga</h2>',
unistr('      <p>Modela en tiempo real el impacto de intervenciones p\00FAblicas: inyecci\00F3n de nuevos residentes, construcci\00F3n de vivienda, consultorios m\00E9dicos, colegios y paradas de autob\00FAs. Eval\00FAa la tensi\00F3n de servicios e identifica autom\00E1ticamente el factor')
||' limitante antes de invertir.</p>',
'      <div class="tags-row">',
'        <span class="tag">5 Sliders de Choque</span>',
'        <span class="tag">Radar 5 Dimensiones</span>',
unistr('        <span class="tag">Sem\00E1foro de Saturaci\00F3n</span>'),
unistr('        <span class="tag">Exportaci\00F3n JSON</span>'),
'      </div>',
'      <div class="card-cta cta-blue">',
'        <span>Abrir simulador interactivo</span>',
'        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
'      </div>',
'    </a>',
'',
'    <a class="card card-span-5 card-map-accent" href="#" data-page="40">',
'      <div class="card-header">',
'        <div class="ico-box ico-green">',
'          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
'        </div>',
unistr('        <span class="badge badge-green">Cartograf\00EDa GeoJSON \00B7 P\00E1g. 40</span>'),
'      </div>',
'      <h2>Mapa Regional &amp; Cuellos de Botella</h2>',
unistr('      <p>Visualizador espacial de los 155 municipios. Explora mapas de coropletas tem\00E1ticos, variaciones relativas de poblaci\00F3n, valor catastral y la capa de diagn\00F3stico con el cuello de botella que frena cada pueblo.</p>'),
'      <div class="tags-row">',
unistr('        <span class="tag">9 Capas Anal\00EDticas</span>'),
'        <span class="tag">Ranking Top 5</span>',
unistr('        <span class="tag">Ficha Din\00E1mica</span>'),
'      </div>',
'      <div class="card-cta cta-green">',
'        <span>Explorar mapa territorial</span>',
'        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
'      </div>',
'    </a>',
'',
'    <a class="card card-span-6 card-data-accent" href="#" data-page="30">',
'      <div class="card-header">',
'        <div class="ico-box ico-purple">',
'          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
'        </div>',
unistr('        <span class="badge badge-purple">Datos Abiertos \00B7 P\00E1g. 30</span>'),
'      </div>',
'      <h2>Observatorio de Datos Abiertos</h2>',
unistr('      <p>Consulta las series 2010\20132035 de los 155 municipios: indicadores actuales, proyecci\00F3n a 2035, banda de incertidumbre y presi\00F3n sobre servicios. Busca, ordena y descarga el resultado en CSV.</p>'),
'      <div class="tags-row">',
unistr('        <span class="tag">Series 2010\20132035</span>'),
'        <span class="tag">155 municipios</span>',
'        <span class="tag">Descarga CSV</span>',
'      </div>',
'      <div class="card-cta cta-purple">',
'        <span>Consultar tablas abiertas</span>',
'        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
'      </div>',
'    </a>',
'',
'    <a class="card card-span-6 card-tech-accent" href="#" data-page="30">',
'      <div class="card-header">',
'        <div class="ico-box ico-amber">',
'          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" '
||'x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="15" x2="23" y2="15"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="15" x2="4" y2="15"/></svg>',
'        </div>',
unistr('        <span class="badge badge-amber">Arquitectura Oracle \00B7 N2</span>'),
'      </div>',
unistr('      <h2>Inferencia In-Database &amp; Validaci\00F3n M3/M4</h2>'),
unistr('      <p>Los 6 modelos ONNX core (M3 + M4\00D75) y el modelo M6 de proyecci\00F3n a 2035 viven dentro de Oracle Autonomous 23ai. La inferencia se ejecuta con DBMS_VECTOR y PREDICTION() en SQL nativo, sin microservicios externos ni latencia de red. Wallet mTL')
||unistr('S y RGPD por dise\00F1o.</p>'),
'      <div class="tags-row">',
'        <span class="tag">6 ONNX core</span>',
unistr('        <span class="tag">M6 proyecci\00F3n</span>'),
'        <span class="tag">DBMS_VECTOR</span>',
'        <span class="tag">PREDICTION()</span>',
'        <span class="tag">Wallet mTLS</span>',
'      </div>',
'      <div class="card-cta cta-amber">',
unistr('        <span>Ver validaci\00F3n y datos</span>'),
'        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
'      </div>',
'    </a>',
'  </div>',
'',
'  <div class="footer">',
'    <div class="footer-sources">',
unistr('      <strong>Fuentes:</strong> Comunidad de Madrid \00B7 INE \00B7 IGN \00B7 CRTM \00B7 S\00F3kerim Notariado.'),
unistr('      Licencia CC-BY 4.0. Atribuci\00F3n CRTM. Los huecos son NA: no se imputan.'),
'    </div>',
'    <div class="footer-badge">',
'      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
unistr('      Oracle Autonomous 23ai \00B7 APEX 26.1'),
'    </div>',
'  </div>',
'</div>',
'<script>',
'document.querySelectorAll(''.pv-portal [data-page]'').forEach(function(a){',
'  a.addEventListener(''click'', function(e){',
'    e.preventDefault();',
'    location.href=''f?p=''+apex.env.APP_ID+'':''+this.getAttribute(''data-page'')+'':''+apex.env.APP_SESSION;',
'  });',
'});',
'</script>~'');',
'END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
end;
/
prompt --application/pages/page_00010
begin
wwv_flow_imp_page.create_page(
 p_id=>10
,p_name=>'Simulador What-If'
,p_alias=>'PERFIL-INSTITUCIONAL'
,p_step_title=>'Simulador What-If'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(143622573347876333)
,p_plug_name=>'Simulador What-If'
,p_static_id=>'dashboard-institucional'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4502917002193490937
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN',
'  -- 1. Estilos de la cabecera',
'  HTP.P(q''~<style>',
'  .t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}',
'  .t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}',
'  .t-Header .a-Logo:hover{color:#5eead4!important}',
'  </style>',
'  </style>~'');',
'',
'  -- 2. Estilos, HTML y JS del simulador (prediccion + what-if)',
'  HTP.P(q''~<style>',
'  .sw{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1280px;margin:0 auto;padding:8px}',
'  .sw .bar{display:flex;gap:8px;align-items:center;margin:0 0 0 auto}',
'  .sw .dldrop{position:relative;margin-left:auto;display:flex;gap:8px;align-items:center}',
'  .sw .dlmenu{display:none;position:absolute;right:0;top:calc(100% + 4px);background:#fff;border:1px solid #cbd5e1;border-radius:9px;box-shadow:0 8px 22px rgba(15,42,68,.14);z-index:20;min-width:150px;overflow:hidden}',
'  .sw .dlmenu button{display:block;width:100%;text-align:left;background:#fff;border:0;padding:9px 12px;font:inherit;font-size:12px;font-weight:700;color:#334155;cursor:pointer}',
'  .sw .dlmenu button:hover{background:#f4f7fa;color:#0f766e}',
'  .sw .btn2{background:#fff;border:1px solid #cbd5e1;color:#0f766e;font-weight:800;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:12px}',
'  .sw .btn2:hover{filter:brightness(1.05)}',
'  .sw .btn2[disabled]{opacity:.45;cursor:not-allowed}',
'  .sw h1{font-size:26px;line-height:1.15;margin:6px 0 2px;color:#0f2a44}',
'  .sw .sub{font-size:13px;color:#5b6b7c;margin:0 0 8px}',
'  .sw .topbar{display:flex;gap:12px;align-items:flex-end;margin:0 0 16px;flex-wrap:wrap}',
'  .sw .topbar>div:not(.dldrop){min-width:200px}',
'  .sw .topbar label{margin:0 0 4px}',
'  .sw .btnrun{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:10px 16px;font-weight:800;cursor:pointer;font-size:13px;height:38px}',
'  .sw .btnrun:hover{filter:brightness(1.08)}',
'  .sw .btnrun[disabled]{opacity:.6;cursor:wait}',
'  .sw .wrap{display:grid;grid-template-columns:300px minmax(0,1fr);gap:16px;align-items:start}',
'  .sw .panel{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;position:sticky;top:12px}',
'  .sw .panel h2{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#5b6b7c;margin:0 0 12px}',
'  .sw label{display:block;font-size:12px;font-weight:700;color:#334155;margin:10px 0 4px}',
'  .sw input,.sw select{width:100%;padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}',
'  .sw input[type=number]{font-variant-numeric:tabular-nums}',
'  .sw input[disabled],.sw select[disabled]{background:#f4f7fa;color:#94a3b8}',
'  .sw .note{font-size:11px;color:#5b6b7c;line-height:1.45;margin-top:12px;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px}',
'  .sw .err{display:none;margin-top:10px;font-size:12px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}',
'  .sw .stage{position:relative;min-height:560px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;overflow:hidden}',
'  .sw .stage.locked #swRes{filter:blur(7px);pointer-events:none;user-select:none}',
'  .sw #swOverlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(250,252,253,.72);color:#475569;font-weight:800;font-size:16px;z-index:5;text-align:center;padding:20px}',
'  .sw #swOverlay .spin{width:26px;height:26px;border-radius:50%;border:3px solid #cbd5e1;border-top-color:#0f766e;animation:swspin .9s linear infinite}',
'  @keyframes swspin{to{transform:rotate(360deg)}}',
'  .sw .kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:14px}',
'  .sw .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px}',
'  .sw .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}',
'  .sw .kpi b{display:block;font-size:24px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}',
'  .sw .kpi .s{font-size:11px;color:#5b6b7c}',
'  .sw .card{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:14px;margin-bottom:12px}',
'  .sw h3{font-size:13px;margin:0 0 10px;color:#0f2a44}',
'  .sw .dim{display:grid;grid-template-columns:96px 1fr 1fr 84px;gap:7px;align-items:center;font-size:11px;margin:8px 0}',
'  .sw .dim span{font-weight:700;color:#334155}',
'  .sw .track{height:8px;background:#eef2f6;border-radius:99px;overflow:hidden}',
'  .sw .track i{display:block;height:100%;border-radius:99px}',
'  .sw .track .before{background:#cbd5e1}.sw .track .after{background:#14b8a6}',
'  .sw .dim b{text-align:right;font-variant-numeric:tabular-nums;color:#0f2a44}',
'  .sw table{width:100%;border-collapse:collapse;font-size:12px}',
'  .sw th{text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea}',
'  .sw td{padding:6px;border-bottom:1px solid #eef2f6}',
'  .sw .num{text-align:right;font-variant-numeric:tabular-nums}',
'  .sw label .difval{float:right;font-variant-numeric:tabular-nums;font-weight:800}',
'  .sw .difval.pos{color:#0f766e}.sw .difval.neg{color:#b91c1c}.sw .difval.zero{color:#94a3b8}',
'  .sw input[type=range]{accent-color:#0f766e;padding:0}',
'  @media(max-width:980px){.sw .wrap,.sw .kpis{grid-template-columns:1fr}.sw .panel{position:static}}',
'  </style>',
'  <div class="sw">',
'  <h1>Simulador What-If</h1>',
'   <div class="topbar">',
'    <div><label>Municipio</label><select id="swCod"></select></div>',
'    <div><label>A&ntilde;o de predicci&oacute;n</label><select id="swAnio"></select></div>',
'    <div><button id="swBtn" type="button" class="btnrun">Ejecutar Simulaci&oacute;n</button></div>',
'    <div class="dldrop">',
'     <button id="swBtnDl" type="button" class="btn2" disabled>Descargar</button>',
'     <button id="swBtnImp" type="button" class="btn2">Importar JSON</button>',
'     <div class="dlmenu" id="swDlMenu" style="display:none">',
'      <button type="button" data-fmt="json">JSON (.json)</button>',
'      <button type="button" data-fmt="csv">CSV (.csv)</button>',
'     </div>',
'     <input id="swFile" type="file" accept=".json,application/json" style="display:none">',
'    </div>',
'   </div>',
'   <div class="wrap">',
'    <div class="panel">',
'     <h2>Diferenciales del escenario (What-If)</h2>',
'     <label>Diferencial de residentes <span id="swPopV" class="difval zero">0</span></label>',
'     <input id="swPop" type="range" step="1" value="0" disabled>',
'     <label>Diferencial de viviendas <span id="swVivV" class="difval zero">0</span></label>',
'     <input id="swViv" type="range" step="1" value="0" disabled>',
'     <label>Diferencial de centros de salud <span id="swSalV" class="difval zero">0</span></label>',
'     <input id="swSal" type="range" step="1" value="0" disabled>',
'     <label>Diferencial de escuelas <span id="swEscV" class="difval zero">0</span></label>',
'     <input id="swEsc" type="range" step="1" value="0" disabled>',
'     <label>Diferencial de paradas <span id="swParV" class="difval zero">0</span></label>',
'     <input id="swPar" type="range" step="1" value="0" disabled>',
'     <div id="swErr" class="err"></div>',
'     <div class="note">Se emplean los modelos <b>M1</b> (proyeccion base al a&ntilde;o seleccionado), <b>M2</b> (5 dimensiones del estado) y <b>M4</b> (stocks proyectados: viviendas/salud/paradas + escuelas esperadas)</div>',
'    </div>',
'    <div class="stage locked" id="swStage">',
'     <div id="swOverlay"><span id="swSpin" class="spin" style="display:none"></span><span id="swOverlayTx">Ejecuta la simulaci&oacute;n para visualizar</span></div>',
'     <div id="swRes" style="padding:16px">',
'      <div class="kpis">',
'       <div class="kpi"><div class="l">&Iacute;ndice antes &rarr; escenario</div><b><span id="swIdxA">--</span> &rarr; <span id="swIdxB">--</span></b><div class="s"><span id="swDelta"></span> <span id="swLimit" style="color:#64748b"></span></div></di'
||'v>     <div class="kpi"><div class="l">Poblaci&oacute;n proyectada M1</div><b id="swPobBase">--</b><div class="s">banda <span id="swBand">--</span> &middot; factor <span id="swFactor">--</span></div></div>',
'       <div class="kpi"><div class="l">Poblaci&oacute;n escenario</div><b id="swPob">--</b><div class="s" id="swPobS"></div></div>',
'      </div>',
'      <div class="card">',
'       <h3>Cinco dimensiones (0-100)</h3>',
'       <div id="swDims"></div>',
'      </div>',
'      <div class="card">',
'       <h3>Ratios de saturaci&oacute;n</h3>',
'       <table id="swRatios"></table>',
'      </div>',
'      <div class="card">',
'       <h3>Choque aplicado</h3>',
'       <table id="swChoques"></table>',
'      </div>',
'     </div>',
'    </div>',
'   </div>',
'  </div>',
'  <script>',
'  (function(){',
'   var RESULT=null, BASE=false;',
'   function $(i){return document.getElementById(i);}',
'   function esc(s){return (s==null?"":(""+s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}',
'   function num(v,d){return (v==null||v==="")?"--":Number(v).toFixed(d==null?0:d);}',
'   function api(n,p,cb){apex.server.process(n,p,{dataType:"json",success:cb,error:function(){$("swErr").style.display="block";$("swErr").textContent="El servidor respondio con error; revisa el log de la base.";$("swBtn").disabled=false;$("swSpin").st'
||'yle.display="none";var tx=document.getElementById("swOverlayTx"),ov=document.getElementById("swOverlay");if(tx){tx.textContent="Ejecuta la simulaci\u00f3n para visualizar";}if(ov)ov.style.display="flex";}});}',
'   function fmtDif(n){var x=Math.round(Number(n)||0);return x>0?"+"+x.toLocaleString("es-ES"):x<0?x.toLocaleString("es-ES"):"0";}',
'   function pintaDif(id,n){var el=$(id+"V");var x=Math.round(Number(n)||0);el.textContent=fmtDif(x);el.className="difval"+(x>0?" pos":x<0?" neg":" zero");}',
'   function ponSlider(id,min,max){var el=$(id);var v=Math.round(Number(el.value)||0);min=Math.round(min);max=Math.round(max);if(min>max){var m=min;min=max;max=m;}el.min=min;el.max=max;el.step=1;el.value=Math.min(Math.max(v,min),max);pintaDif(id,el.va'
||'lue);}',
'   function actualizarLimites(r){',
'    var d={pop:Number($("swPop").value)||0,viv:Number($("swViv").value)||0,sal:Number($("swSal").value)||0,esc:Number($("swEsc").value)||0,par:Number($("swPar").value)||0};',
'    var base={pop:Math.max(0,Number(r.poblacion_base_anio)||0),viv:Math.max(0,(Number(r.viviendas_despues)||0)-d.viv),sal:Math.max(0,(Number(r.centros_salud_despues)||0)-d.sal),esc:Math.max(0,(Number(r.escuelas_despues)||0)-d.esc),par:Math.max(0,(Num'
||'ber(r.paradas_despues)||0)-d.par)};',
'    ponSlider("swPop",-base.pop,3*base.pop);',
'    ["swViv","swSal","swEsc","swPar"].forEach(function(id){var b=base[id.slice(2).toLowerCase()];ponSlider(id,-b,Math.max(3*b,20));});',
'   }',
'   function colMej(a,b){var x=Number(b)-Number(a);return x>0?"#0f766e":x<0?"#b91c1c":"#64748b";}',
'   function fila(t,a,b,dec,col){return "<tr><td>"+t+"</td><td class=\"num\">"+num(a,dec)+"</td><td class=\"num\""+(col?" style=\"color:"+col+"\"":"")+">"+num(b,dec)+"</td></tr>";}',
'   function render(r){',
'    if(!r||typeof r!=="object"||!("indice_despues" in r)){$("swErr").style.display="block";$("swErr").textContent="El JSON no parece una respuesta del simulador.";return;}',
'    RESULT=r;$("swBtnDl").disabled=false;',
'    $("swStage").classList.remove("locked");$("swOverlay").style.display="none";',
'    $("swIdxA").textContent=num(r.indice_antes,1);$("swIdxB").textContent=num(r.indice_despues,1);',
'    var d=num(r.delta_indice,1);var deltaN=Number(r.delta_indice);$("swDelta").textContent=(deltaN>0?"+ ":"")+d+(deltaN>0?" (mejora)":deltaN<0?" (caida)":"");',
'     $("swDelta").style.color=deltaN>=0?"#0f766e":"#b91c1c";',
'     $("swIdxB").style.color=deltaN>0?"#0f766e":deltaN<0?"#b91c1c":"";',
'    $("swLimit").textContent="factor limitante: "+esc(r.factor_limitante);',
'    $("swPobBase").textContent=num(r.poblacion_base_anio,0);',
'    $("swBand").textContent=num(r.poblacion_anio_p10,0)+" - "+num(r.poblacion_anio_p90,0);',
'    $("swFactor").textContent="x"+num(r.factor_m3,4);',
'    $("swPob").textContent=num(r.poblacion_despues,0);',
'    $("swPobS").textContent=num(r.poblacion_antes,0)+" -> "+num(r.poblacion_despues,0)+" hab.";',
'    var dims=[["Demografia","dem"],["Vivienda","viv"],["Servicios","ser"],["Accesibilidad","acc"],["Empleo","emp"]];',
'    $("swDims").innerHTML=dims.map(function(x){var a=r["dim_"+x[1]+"_antes"],b=r["dim_"+x[1]+"_despues"];',
'     var col=colMej(a,b);',
'     return "<div class=\"dim\"><span>"+x[0]+"</span><span class=\"track\"><i class=\"before\" style=\"width:"+num(a)+"%\"></i></span><span class=\"track\"><i class=\"after\" style=\"width:"+num(b)+"%;background:"+col+"\"></i></span><b>"+num(a,1)+" <'
||'span style=\"color:"+col+"\">&rarr; "+num(b,1)+"</span></b></div>";',
'    }).join("");',
'    $("swRatios").innerHTML="<thead><tr><th>Ratio</th><th class=\"num\">Antes</th><th class=\"num\">Escenario</th></tr></thead><tbody>"',
'     +fila("Centros de salud por 10.000 hab.",r.salud_10k_antes,r.salud_10k_despues,2,colMej(r.salud_10k_antes,r.salud_10k_despues))',
'     +fila("Escuelas por 1.000 hab.",r.escuelas_1000_antes,r.escuelas_1000_despues,3,colMej(r.escuelas_1000_antes,r.escuelas_1000_despues))',
'     +fila("Paradas por 1.000 hab.",r.paradas_1000_antes,r.paradas_1000_despues,3,colMej(r.paradas_1000_antes,r.paradas_1000_despues))',
'     +fila("Viviendas por 1.000 hab.",r.viv_1000_antes,r.viv_1000_despues,1,colMej(r.viv_1000_antes,r.viv_1000_despues))',
'     +"</tbody>";',
'    $("swChoques").innerHTML="<thead><tr><th>Recurso</th><th class=\"num\">Antes</th><th class=\"num\">Escenario</th></tr></thead><tbody>"',
'     +fila("Poblacion",r.poblacion_antes,r.poblacion_despues,0)',
'     +fila("Viviendas",r.viviendas_antes,r.viviendas_despues,0)',
'     +fila("Centros de salud",r.centros_salud_antes,r.centros_salud_despues,0)',
'     +fila("Escuelas",r.escuelas_antes,r.escuelas_despues,0)',
'     +fila("Paradas",r.paradas_antes,r.paradas_despues,0)',
'     +"</tbody>";',
'    actualizarLimites(r);',
'   }',
'   function run(){',
'    if($("swBtn").disabled)return;',
'    $("swErr").style.display="none";',
'    $("swBtn").disabled=true;$("swSpin").style.display="block";$("swOverlayTx").textContent="Cargando\u2026";$("swOverlay").style.display="flex";',
'    api("SIMULAR",{x01:$("swCod").value,x02:$("swAnio").value,x03:$("swPop").value||0,x04:$("swViv").value||0,x05:$("swSal").value||0,x06:$("swEsc").value||0,x07:$("swPar").value||0},function(r){',
'     $("swBtn").disabled=false;$("swSpin").style.display="none";',
'     render(r);',
'     if(!BASE){',
'      BASE=true;',
'      ["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).disabled=false;});',
'      $("swBtn").textContent="Reejecutar Simulaci\u00f3n";',
'     }',
'    });',
'   }',
'   function aCsv(o){',
'    var ks=Object.keys(o),lin=[ks.join(";")];',
'    lin.push(ks.map(function(k){var v=o[k];if(v==null)return "";v=""+v;return (v.indexOf(";")>=0||v.indexOf("\"")>=0||v.indexOf("\n")>=0)?"\""+v.replace(/"/g,"\"\"")+"\"":v;}).join(";"));',
'    return "\uFEFF"+lin.join("\n");',
'   }',
'   function descargar(fmt){',
'    if(!RESULT)return;',
'    var nom="simulador-"+(RESULT.cod||"escenario")+"-"+(RESULT.anio_simulado||"");',
'    var blob,ext;',
'    if(fmt==="csv"){blob=new Blob([aCsv(RESULT)],{type:"text/csv;charset=utf-8"});ext="csv";}',
'    else{blob=new Blob([JSON.stringify(RESULT,null,1)],{type:"application/json"});ext="json";}',
'    var u=URL.createObjectURL(blob);',
'    var a=document.createElement("a");',
'    a.href=u;a.download=nom+"."+ext;',
'    document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);',
'   }',
'   $("swFile").addEventListener("change",function(){',
'    var f=this.files&&this.files[0];if(!f)return;',
'    var rd=new FileReader();',
'    rd.onload=function(){',
'     try{var r=JSON.parse(rd.result);$("swErr").style.display="none";render(r);',
'      if(!BASE){BASE=true;["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).disabled=false;});$("swBtn").textContent="Reejecutar Simulaci\u00f3n";}',
'     }',
'     catch(e){$("swErr").style.display="block";$("swErr").textContent="El fichero no es un JSON valido.";}',
'    };',
'    rd.readAsText(f);this.value="";',
'   });',
'   function boot(){',
'    var o="",y;for(y=2025;y<=2035;y++){o+="<option value=\""+y+"\">"+y+"</option>";}',
'    $("swAnio").innerHTML=o;$("swAnio").value="2030";',
'    api("DATOS",{},function(rows){',
'     var m=rows||[];',
'     $("swCod").innerHTML=m.map(function(x){return "<option value=\""+esc(x.cod)+"\">"+esc(x.nombre)+"</option>";}).join("");',
'     var pre=null;try{pre=JSON.parse(sessionStorage.getItem(''pvWiJugada'')||"null");}catch(e){pre=null;}',
'     if(pre&&pre.cod){var sel=$("swCod");var hay=false;Array.prototype.forEach.call(sel.options,function(o){if(o.value===String(pre.cod))hay=true;});',
'      if(hay){sel.value=String(pre.cod);$("swAnio").value=String(pre.anio||"2030");sessionStorage.removeItem(''pvWiJugada'');run();}else{sessionStorage.removeItem(''pvWiJugada'');}}',
'    });',
'    ["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).addEventListener("input",function(){pintaDif(id,this.value);});});',
'    $("swBtnDl").addEventListener("click",function(ev){ev.stopPropagation();var m=$("swDlMenu");m.style.display=(m.style.display==="block")?"none":"block";});',
'    document.querySelectorAll("#swDlMenu button").forEach(function(b){b.addEventListener("click",function(ev){ev.stopPropagation();descargar(b.getAttribute("data-fmt"));$("swDlMenu").style.display="none";});});',
'    document.addEventListener("click",function(){$("swDlMenu").style.display="none";});',
'    $("swBtnImp").addEventListener("click",function(){$("swFile").click();});',
'    $("swBtn").addEventListener("click",run);',
'    document.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); run(); } });',
'   }',
'   (function w(){ if(window.apex&&window.apex.server){setTimeout(boot,400);} else {setTimeout(w,100);} })();',
'  })();',
'  </script>',
'  </script>~'');',
'END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(143622573347876331)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'DATOS'
,p_static_id=>'datos'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB; v_len PLS_INTEGER; v_pos PLS_INTEGER := 1;',
'BEGIN',
'  APEX_JSON.INITIALIZE_CLOB_OUTPUT; APEX_JSON.OPEN_ARRAY;',
'  FOR m IN (SELECT * FROM WKSP_DATATHON.PV_MUN_2035 ORDER BY nombre) LOOP',
'    APEX_JSON.OPEN_OBJECT;',
'    APEX_JSON.WRITE(''cod'', m.cod_ine); APEX_JSON.WRITE(''nombre'', m.nombre); APEX_JSON.WRITE(''pob'', m.poblacion);',
'    APEX_JSON.WRITE(''lat'', m.lat); APEX_JSON.WRITE(''lon'', m.lon); APEX_JSON.WRITE(''dist'', m.distancia_sol_km);',
'    APEX_JSON.WRITE(''tiempo'', m.tiempo_centro_min); APEX_JSON.WRITE(''modo'', m.modo); APEX_JSON.WRITE(''paradas'', m.paradas_total);',
'    APEX_JSON.WRITE(''escuelas'', m.escuelas); APEX_JSON.WRITE(''precio'', m.precio_medio); APEX_JSON.WRITE(''precio_m2'', m.precio_m2);',
'    APEX_JSON.WRITE(''compraventas'', m.compraventas); APEX_JSON.WRITE(''fiabilidad'', m.fiabilidad);',
'    APEX_JSON.WRITE(''dem'', m.dim_dem); APEX_JSON.WRITE(''viv'', m.dim_viv); APEX_JSON.WRITE(''ser'', m.dim_ser);',
'    APEX_JSON.WRITE(''acc'', m.dim_acc); APEX_JSON.WRITE(''emp'', m.dim_emp); APEX_JSON.WRITE(''indice'', m.indice);',
'    APEX_JSON.WRITE(''factor'', m.factor_limitante);',
'    APEX_JSON.WRITE(''p2035'', m.poblacion_2035); APEX_JSON.WRITE(''p10'', m.pob_2035_p10); APEX_JSON.WRITE(''p90'', m.pob_2035_p90);',
'    APEX_JSON.WRITE(''crec'', m.crecimiento_pct); APEX_JSON.WRITE(''esc'', m.escenario); APEX_JSON.WRITE(''fiabp'', m.fiab_pronostico);',
'    APEX_JSON.WRITE(''tasa'', m.tasa_2035_pct); APEX_JSON.WRITE(''conv'', m.pob_2035_convergencia); APEX_JSON.WRITE(''pers'', m.pob_2035_persistencia);',
'    APEX_JSON.WRITE(''san25'', m.hab_sanit_2025); APEX_JSON.WRITE(''san35'', m.hab_sanit_2035);',
'    APEX_JSON.WRITE(''edu25'', m.hab_escuela_2025); APEX_JSON.WRITE(''edu35'', m.hab_escuela_2035);',
'    APEX_JSON.WRITE(''par25'', m.hab_parada_2025); APEX_JSON.WRITE(''par35'', m.hab_parada_2035);',
'    APEX_JSON.WRITE(''viv25'', m.hab_vivienda_2025); APEX_JSON.WRITE(''viv35'', m.hab_vivienda_2035);',
'    APEX_JSON.OPEN_ARRAY(''serie'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''proy'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_PROYECCION_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''vecinos'');',
'    FOR v IN (SELECT v.nombre_vecino, v.distancia_km, b.indice, b.factor_limitante, b.tiempo_centro_min',
'              FROM WKSP_DATATHON.PV_VECINOS v JOIN WKSP_DATATHON.PV_MUN_BASE b ON b.cod_ine=v.cod_vecino',
'              WHERE v.cod_ine=m.cod_ine ORDER BY v.distancia_km) LOOP',
'      APEX_JSON.OPEN_OBJECT; APEX_JSON.WRITE(''nombre'', v.nombre_vecino); APEX_JSON.WRITE(''dist'', v.distancia_km);',
'      APEX_JSON.WRITE(''indice'', v.indice); APEX_JSON.WRITE(''factor'', v.factor_limitante); APEX_JSON.WRITE(''tiempo'', v.tiempo_centro_min);',
'      APEX_JSON.CLOSE_OBJECT;',
'    END LOOP;',
'    APEX_JSON.CLOSE_ARRAY; APEX_JSON.CLOSE_OBJECT;',
'  END LOOP;',
'  APEX_JSON.CLOSE_ARRAY;',
'  v_json := APEX_JSON.GET_CLOB_OUTPUT; v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos)); v_pos := v_pos + 8000; END LOOP;',
'  APEX_JSON.FREE_OUTPUT;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000011
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(143622573347876332)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'SIMULAR'
,p_static_id=>'simular'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE v_json CLOB;',
'BEGIN',
'  v_json := WKSP_DATATHON.PV_SIMULA(',
'      apex_application.g_x01,',
'      TO_NUMBER(apex_application.g_x02),',
'      NVL(TO_NUMBER(apex_application.g_x03),0),',
'      NVL(TO_NUMBER(apex_application.g_x04),0),',
'      NVL(TO_NUMBER(apex_application.g_x05),0),',
'      NVL(TO_NUMBER(apex_application.g_x06),0),',
'      NVL(TO_NUMBER(apex_application.g_x07),0));',
'  HTP.P(v_json);',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000012
);
end;
/
prompt --application/pages/page_00020
begin
wwv_flow_imp_page.create_page(
 p_id=>20
,p_name=>'Perfil Ciudadano (retirada)'
,p_alias=>'PERFIL-CIUDADANO'
,p_step_title=>'Perfil Ciudadano (retirada)'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(143622573347876336)
,p_plug_name=>'Dashboard ciudadano'
,p_static_id=>'dashboard-ciudadano'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.sw20{font-family:system-ui,"Segoe UI",Arial,sans-serif;max-width:760px;margin:40px auto;text-align:center;padding:24px;background:#fff;border:1px solid #dbe3ea;border-radius:14px;color:#0f172a}',
'.sw20 h1{font-size:24px;color:#0f2a44;margin:0 0 8px}',
'.sw20 p{color:#5b6b7c;font-size:14px;margin:0 0 14px}',
'.sw20 a{color:#0f766e;font-weight:800;text-decoration:none}',
'</style>',
'<div class="sw20">',
'<h1>Perfil Ciudadano &#8212; retirada</h1>',
'<p>La funcionalidad se unifico en una unica pagina.</p>',
'<a href="f?p=&APP_ID.:10:&APP_SESSION.::&DEBUG.:::">Ir al Simulador What-If</a>',
'</div>~''); END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(143622573347876335)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'DATOS'
,p_static_id=>'datos'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB; v_len PLS_INTEGER; v_pos PLS_INTEGER := 1;',
'BEGIN',
'  APEX_JSON.INITIALIZE_CLOB_OUTPUT; APEX_JSON.OPEN_ARRAY;',
'  FOR m IN (SELECT * FROM WKSP_DATATHON.PV_MUN_2035 ORDER BY nombre) LOOP',
'    APEX_JSON.OPEN_OBJECT;',
'    APEX_JSON.WRITE(''cod'', m.cod_ine); APEX_JSON.WRITE(''nombre'', m.nombre); APEX_JSON.WRITE(''pob'', m.poblacion);',
'    APEX_JSON.WRITE(''lat'', m.lat); APEX_JSON.WRITE(''lon'', m.lon); APEX_JSON.WRITE(''dist'', m.distancia_sol_km);',
'    APEX_JSON.WRITE(''tiempo'', m.tiempo_centro_min); APEX_JSON.WRITE(''modo'', m.modo); APEX_JSON.WRITE(''paradas'', m.paradas_total);',
'    APEX_JSON.WRITE(''escuelas'', m.escuelas); APEX_JSON.WRITE(''precio'', m.precio_medio); APEX_JSON.WRITE(''precio_m2'', m.precio_m2);',
'    APEX_JSON.WRITE(''compraventas'', m.compraventas); APEX_JSON.WRITE(''fiabilidad'', m.fiabilidad);',
'    APEX_JSON.WRITE(''dem'', m.dim_dem); APEX_JSON.WRITE(''viv'', m.dim_viv); APEX_JSON.WRITE(''ser'', m.dim_ser);',
'    APEX_JSON.WRITE(''acc'', m.dim_acc); APEX_JSON.WRITE(''emp'', m.dim_emp); APEX_JSON.WRITE(''indice'', m.indice);',
'    APEX_JSON.WRITE(''factor'', m.factor_limitante);',
'    APEX_JSON.WRITE(''p2035'', m.poblacion_2035); APEX_JSON.WRITE(''p10'', m.pob_2035_p10); APEX_JSON.WRITE(''p90'', m.pob_2035_p90);',
'    APEX_JSON.WRITE(''crec'', m.crecimiento_pct); APEX_JSON.WRITE(''esc'', m.escenario); APEX_JSON.WRITE(''fiabp'', m.fiab_pronostico);',
'    APEX_JSON.WRITE(''tasa'', m.tasa_2035_pct); APEX_JSON.WRITE(''conv'', m.pob_2035_convergencia); APEX_JSON.WRITE(''pers'', m.pob_2035_persistencia);',
'    APEX_JSON.WRITE(''san25'', m.hab_sanit_2025); APEX_JSON.WRITE(''san35'', m.hab_sanit_2035);',
'    APEX_JSON.WRITE(''edu25'', m.hab_escuela_2025); APEX_JSON.WRITE(''edu35'', m.hab_escuela_2035);',
'    APEX_JSON.WRITE(''par25'', m.hab_parada_2025); APEX_JSON.WRITE(''par35'', m.hab_parada_2035);',
'    APEX_JSON.WRITE(''viv25'', m.hab_vivienda_2025); APEX_JSON.WRITE(''viv35'', m.hab_vivienda_2035);',
'    APEX_JSON.OPEN_ARRAY(''serie'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''proy'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_PROYECCION_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''vecinos'');',
'    FOR v IN (SELECT v.nombre_vecino, v.distancia_km, b.indice, b.factor_limitante, b.tiempo_centro_min',
'              FROM WKSP_DATATHON.PV_VECINOS v JOIN WKSP_DATATHON.PV_MUN_BASE b ON b.cod_ine=v.cod_vecino',
'              WHERE v.cod_ine=m.cod_ine ORDER BY v.distancia_km) LOOP',
'      APEX_JSON.OPEN_OBJECT; APEX_JSON.WRITE(''nombre'', v.nombre_vecino); APEX_JSON.WRITE(''dist'', v.distancia_km);',
'      APEX_JSON.WRITE(''indice'', v.indice); APEX_JSON.WRITE(''factor'', v.factor_limitante); APEX_JSON.WRITE(''tiempo'', v.tiempo_centro_min);',
'      APEX_JSON.CLOSE_OBJECT;',
'    END LOOP;',
'    APEX_JSON.CLOSE_ARRAY; APEX_JSON.CLOSE_OBJECT;',
'  END LOOP;',
'  APEX_JSON.CLOSE_ARRAY;',
'  v_json := APEX_JSON.GET_CLOB_OUTPUT; v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos)); v_pos := v_pos + 8000; END LOOP;',
'  APEX_JSON.FREE_OUTPUT;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000015
);
end;
/
prompt --application/pages/page_00030
begin
wwv_flow_imp_page.create_page(
 p_id=>30
,p_name=>'Datos'
,p_alias=>'DATOS'
,p_step_title=>'Datos'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(143622573347876339)
,p_plug_name=>'Tablas de datos'
,p_static_id=>'tablas-de-datos'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.pv30{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto}',
'.pv30 .head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;flex-wrap:wrap;margin:4px 0 16px}',
'.pv30 .kick{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#0f766e;font-weight:800}',
'.pv30 h1{font-size:28px;line-height:1.15;margin:4px 0 4px;color:#0f2a44;letter-spacing:-.02em}',
'.pv30 .sub{font-size:13px;color:#5b6b7c;margin:0;max-width:820px}',
'.pv30 .tag{font-size:11px;background:#eefaf8;border:1px solid #cdeee8;color:#0f766e;border-radius:99px;padding:6px 10px;font-weight:700;white-space:nowrap}',
'.pv30 .card{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;box-shadow:0 1px 2px rgba(15,42,68,.05),0 8px 22px rgba(15,42,68,.06);margin-bottom:14px}',
'.pv30 .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:14px}',
'.pv30 .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px}',
'.pv30 .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}',
'.pv30 .kpi b{display:block;font-size:24px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}',
'.pv30 .kpi .s{font-size:11px;color:#5b6b7c}',
'.pv30 h3{font-size:14px;margin:0 0 10px;color:#0f2a44}',
'.pv30 .tools{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap;margin-bottom:10px}',
'.pv30 .tools label{font-size:11px;font-weight:700;color:#334155;display:block;margin-bottom:3px}',
'.pv30 input,.pv30 select{padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;font-size:12px;background:#fff;color:#0f172a}',
'.pv30 .btn{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:9px 13px;font-weight:800;font-size:12px;cursor:pointer}',
'.pv30 .btn.ghost{background:#fff;color:#0f766e;border:1px solid #99e0d6}',
'.pv30 .wrap{overflow:auto;max-height:560px;border:1px solid #eef3f7;border-radius:9px}',
'.pv30 table{width:100%;border-collapse:collapse;font-size:11.5px}',
'.pv30 th{position:sticky;top:0;text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea;z-index:1;white-space:nowrap;cursor:pointer;user-select:none}',
'.pv30 th:hover{color:#0f766e}',
'.pv30 td{padding:6px;border-bottom:1px solid #eef2f6;white-space:nowrap}',
'.pv30 td.name{white-space:normal;min-width:150px}',
'.pv30 .num{text-align:right;font-variant-numeric:tabular-nums}',
'.pv30 .pill{display:inline-block;font-size:10px;font-weight:800;border-radius:99px;padding:2px 7px}',
'.pv30 .p-fuerte{background:#d7f5f0;color:#0f766e}',
'.pv30 .p-mod{background:#e6f4fb;color:#0369a1}',
'.pv30 .p-est{background:#fef3c7;color:#92400e}',
'.pv30 .p-dec{background:#fee2e2;color:#b91c1c}',
'.pv30 .fiab{font-size:10px;font-weight:700;color:#475569}',
'.pv30 .note{font-size:11px;color:#5b6b7c;line-height:1.5;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px;margin-top:10px}',
'.pv30 .warn{font-size:11px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px;margin-top:10px}',
'.pv30 .muted{color:#94a3b8}',
'@media(max-width:980px){.pv30 .kpis{grid-template-columns:repeat(2,1fr)}}',
'</style>',
'<div class="pv30">',
'  <div class="head">',
unistr('    <div><div class="kick">Datos abiertos</div><h1>Tablas de datos</h1><p class="sub">Los 155 municipios con sus indicadores actuales y la proyecci\00F3n a 2035. Puedes buscar, ordenar por cualquier columna y descargar el resultado en CSV.</p></div>'),
unistr('    <div class="tag">155 municipios \00B7 26 a\00F1os de serie</div>'),
'  </div>',
'',
'  <div class="kpis">',
unistr('    <div class="kpi"><div class="l">Municipios</div><b id="k30-n">\2014</b><div class="s">visibles con el filtro</div></div>'),
unistr('    <div class="kpi"><div class="l">Poblaci\00F3n 2025</div><b id="k30-p25">\2014</b><div class="s">padr\00F3n</div></div>'),
unistr('    <div class="kpi"><div class="l">Poblaci\00F3n 2035</div><b id="k30-p35">\2014</b><div class="s">proyecci\00F3n</div></div>'),
unistr('    <div class="kpi"><div class="l">Crecimiento medio municipal</div><b id="k30-crec">\2014</b><div class="s">2025-2035</div></div>'),
'  </div>',
'',
'  <div class="card">',
'    <h3>Municipios e indicadores</h3>',
'    <div class="tools">',
'      <div><label for="f30-q">Buscar municipio</label><input id="f30-q" type="search" placeholder="Nombre..." style="min-width:220px"></div>',
'      <div><label for="f30-esc">Escenario</label><select id="f30-esc"><option value="">Todos</option><option>Crecimiento fuerte</option><option>Crecimiento moderado</option><option>Estancamiento</option><option>Declive</option></select></div>',
'      <div><label for="f30-fiab">Fiabilidad</label><select id="f30-fiab"><option value="">Todas</option><option>Alta</option><option>Media</option><option>Baja</option></select></div>',
'      <button class="btn ghost" id="f30-csv" type="button">Descargar CSV</button>',
'    </div>',
'    <div class="wrap"><div id="f30-table"></div></div>',
unistr('    <div class="note" id="f30-count">\2014</div>'),
'  </div>',
'',
'  <div class="card">',
'    <h3>Serie agregada de los 155 municipios, 2010-2035</h3>',
'    <div class="wrap" style="max-height:560px"><div id="f30-serie"></div></div>',
unistr('    <div class="warn">2010-2025 es poblaci\00F3n observada (padr\00F3n). 2026-2035 es proyecci\00F3n del modelo tendencial anclado al crecimiento oficial de la Comunidad de Madrid. La fila de 2026 marca el cambio de fuente.</div>'),
'  </div>',
'',
'  <div class="card">',
'    <h3>Diccionario y fuentes</h3>',
'    <div class="note">',
unistr('      <b>Poblaci\00F3n 2025:</b> padr\00F3n municipal (INE, cifras oficiales).<br>'),
unistr('      <b>Poblaci\00F3n 2035:</b> modelo propio. Tendencia logar\00EDtmica 2015-2025, convergencia amortiguada a la mitad en 10 a\00F1os y anclaje al crecimiento oficial de la CAM (7.137.031 en 2025 a 7.937.124 en 2035, IESTADIS/INE).<br>'),
unistr('      <b>Banda:</b> intervalo de predicci\00F3n del 80 % de la regresi\00F3n, que recoge la volatilidad hist\00F3rica de cada municipio.<br>'),
unistr('      <b>Fiabilidad:</b> alta si el municipio tiene 5.000 habitantes o m\00E1s y R2 igual o mayor que 0,6; media si tiene 1.000 o m\00E1s o R2 igual o mayor que 0,3; baja en el resto.<br>'),
unistr('      <b>\00CDndice:</b> \00EDndice compuesto 2025 del proyecto (20 % demograf\00EDa, 15 % vivienda, 25 % servicios, 25 % accesibilidad, 15 % empleo).<br>'),
unistr('      <b>Presi\00F3n:</b> habitantes por equipamiento si la oferta no cambia. Sanidad = centros de salud + consultorios (2024). Vivienda = unidades urbanas residenciales del Catastro (2025). No se proyecta la oferta.<br>'),
unistr('      <b>Precio:</b> precio medio de escritura notarial (Notariado v\00EDa S\00F3kerim, CC-BY). Sin muestra suficiente queda vac\00EDo.<br>'),
'      <b>Tiempo:</b> percentil 10 de trayectos directos a menos de 5 km de Sol (GTFS CRTM). Solo 56 de 155 municipios tienen trayecto directo.<br>',
unistr('      <b>Licencia:</b> CC-BY. Atribuci\00F3n CRTM: Powered by CRTM.'),
'    </div>',
'  </div>',
'</div>',
'<script>',
'(function(){',
'  var DATA=[],VIEW=[],SORT={k:''nombre'',dir:1};',
unistr('  var COLS=[[''nombre'',''Municipio''],[''pob'',''Poblaci\00F3n 2025''],[''p2035'',''Poblaci\00F3n 2035''],[''crec'',''Crec. %''],[''banda'',''Banda 80 %''],[''esc'',''Escenario''],[''fiabp'',''Fiabilidad''],[''indice'',''\00CDndice 2025''],[''tiempo'',''Tiempo''],[''precio'',''Precio''],[''san35'',''Hab')
||'./equip. sanitario''],[''viv35'',''Hab./vivienda'']];',
'  function $(id){return document.getElementById(id);}',
unistr('  function fmt(v,d){if(v===null||v===undefined||isNaN(v))return ''\2014'';return Number(v).toLocaleString(''es-ES'',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}'),
'  function esc(s){return String(s).replace(/[&<>"'']/g,function(c){return {''&'':''&amp;'',''<'':''&lt;'',''>'':''&gt;'',''"'':''&quot;'',"''":''&#39;''}[c];});}',
'  function api(name,params,cb){apex.server.process(name,params,{success:function(d){try{cb(typeof d===''string''?JSON.parse(d):d);}catch(e){console.error(e);}},error:function(x){if(!window.__pvTries)window.__pvTries=0;if(window.__pvTries++<8){setTimeou'
||'t(function(){api(name,params,cb);},900);}else{console.error(x);}}});}',
unistr('  function pill(e){var c=e===''Crecimiento fuerte''?''p-fuerte'':e===''Crecimiento moderado''?''p-mod'':e===''Declive''?''p-dec'':''p-est'';return ''<span class="pill ''+c+''">''+esc(e||''\2014'')+''</span>'';}'),
'  function filtered(){var q=$(''f30-q'').value.trim().toLowerCase(),e=$(''f30-esc'').value,f=$(''f30-fiab'').value;return DATA.filter(function(m){if(q&&m.nombre.toLowerCase().indexOf(q)<0)return false;if(e&&m.esc!==e)return false;if(f&&m.fiabp!==f)return f'
||'alse;return true;});}',
'  function sorted(rows){var k=SORT.k,d=SORT.dir;return rows.slice().sort(function(a,b){var va=a[k],vb=b[k];if(va==null&&vb==null)return 0;if(va==null)return 1;if(vb==null)return -1;if(typeof va===''string'')return va.localeCompare(vb,''es'')*d;return (va'
||'-vb)*d;});}',
unistr('  function renderTable(){VIEW=sorted(filtered());var head=''<table><thead><tr>''+COLS.map(function(c){var arr=SORT.k===c[0]?(SORT.dir>0?'' \25B2'':'' \25BC''):'''';var cls=(c[0]===''nombre'')?'''':'' class="num"'';return ''<th data-k="''+c[0]+''"''+cls+''>''+c[1]+arr+''</th>'';})')
||'.join('''')+''</tr></thead><tbody>'';var body=VIEW.map(function(m){return ''<tr><td class="name"><b>''+esc(m.nombre)+''</b></td><td class="num">''+fmt(m.pob)+''</td><td class="num"><b>''+fmt(m.p2035)+''</b></td><td class="num">''+(m.crec>0?''+'':'''')+fmt(m.crec,1)+'
||unistr(''' %</td><td class="num muted">''+fmt(m.p10)+'' \2013 ''+fmt(m.p90)+''</td><td>''+pill(m.esc)+''</td><td class="fiab">''+esc(m.fiabp||''\2014'')+''</td><td class="num">''+fmt(m.indice,1)+''</td><td class="num">''+(m.tiempo==null?''\2014'':fmt(m.tiempo,0)+'' min'')+''</td><td class')
||unistr('="num">''+(m.precio==null?''\2014'':fmt(m.precio,0)+'' \20AC'')+''</td><td class="num">''+fmt(m.san35,0)+''</td><td class="num">''+fmt(m.viv35,2)+''</td></tr>'';}).join('''');$(''f30-table'').innerHTML=head+body+''</tbody></table>'';$(''f30-table'').querySelectorAll(''th'').forE')
||'ach(function(th){th.addEventListener(''click'',function(){var k=th.getAttribute(''data-k'');if(SORT.k===k)SORT.dir*=-1;else{SORT.k=k;SORT.dir=1;}renderTable();});});var n=VIEW.length,p25=0,p35=0,c=0,nc=0;VIEW.forEach(function(m){p25+=m.pob||0;p35+=m.p203'
||unistr('5||0;if(m.crec!=null){c+=m.crec;nc++;}});$(''k30-n'').textContent=n;$(''k30-p25'').textContent=fmt(p25);$(''k30-p35'').textContent=fmt(p35);$(''k30-crec'').textContent=nc?(c/nc>0?''+'':'''')+fmt(c/nc,1)+'' %'':''\2014'';$(''f30-count'').textContent=n+'' de ''+DATA.length+'' ')
||unistr('municipios \00B7 ordenado por ''+COLS.filter(function(x){return x[0]===SORT.k;})[0][1]+(SORT.dir>0?'' (ascendente)'':'' (descendente)'');}'),
'  function renderSerie(){if(!DATA.length)return;var years=[],tot={};for(var y=2010;y<=2035;y++){years.push(y);tot[y]=0;}DATA.forEach(function(m){(m.serie||[]).forEach(function(v,i){tot[2010+i]+=Number(v)||0;});(m.proy||[]).forEach(function(v,i){tot[2'
||unistr('026+i]+=Number(v)||0;});});var rows=years.map(function(y,i){var prev=i?tot[years[i-1]]:null;var g=prev?(tot[y]/prev-1)*100:null;return ''<tr><td>''+y+(y===2026?'' <span class="pill p-mod">proyecci\00F3n</span>'':'''')+''</td><td class="num"><b>''+fmt(tot[y])+''</')
||unistr('b></td><td class="num">''+(g==null?''\2014'':(g>0?''+'':'''')+fmt(g,2)+'' %'')+''</td></tr>'';}).join('''');$(''f30-serie'').innerHTML=''<table><thead><tr><th>A\00F1o</th><th class="num">Poblaci\00F3n de los 155</th><th class="num">Variaci\00F3n anual</th></tr></thead><tbody>''+rows')
||'+''</tbody></table>'';}',
'  function csv(){var sep='';'';var lines=[[''Municipio'',''Poblacion 2025'',''Poblacion 2035'',''P10'',''P90'',''Crecimiento %'',''Escenario'',''Fiabilidad'',''Indice 2025'',''Tiempo min'',''Precio euros'',''Hab por equipamiento sanitario 2035'',''Hab por vivienda 2035''].join('
||'sep)];function num(v,d){if(v==null||v===''''||isNaN(v))return '''';return Number(v).toFixed(d==null?0:d).replace(''.'','','');}VIEW.forEach(function(m){lines.push([m.nombre,num(m.pob),num(m.p2035),num(m.p10),num(m.p90),num(m.crec,1),m.esc,m.fiabp,num(m.indic'
||'e,1),num(m.tiempo,0),num(m.precio,0),num(m.san35,0),num(m.viv35,2)].join(sep));});var blob=new Blob([''\ufeff''+lines.join(''\r\n'')],{type:''text/csv;charset=utf-8''});var a=document.createElement(''a'');a.href=URL.createObjectURL(blob);a.download=''pueblos_'
||'con_vida_2035.csv'';document.body.appendChild(a);a.click();document.body.removeChild(a);}',
'  function boot(){$(''f30-q'').addEventListener(''input'',renderTable);$(''f30-esc'').addEventListener(''change'',renderTable);$(''f30-fiab'').addEventListener(''change'',renderTable);$(''f30-csv'').addEventListener(''click'',csv);api(''DATOS'',{},function(rows){DATA='
||'rows;renderTable();renderSerie();});}',
'  (function pvWait(){ if(window.apex && window.apex.server){ setTimeout(boot,1200); } else { setTimeout(pvWait,100); } })();',
'})();',
'</script>',
'~''); END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(143622573347876338)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'DATOS'
,p_static_id=>'datos'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB; v_len PLS_INTEGER; v_pos PLS_INTEGER := 1;',
'BEGIN',
'  APEX_JSON.INITIALIZE_CLOB_OUTPUT; APEX_JSON.OPEN_ARRAY;',
'  FOR m IN (SELECT * FROM WKSP_DATATHON.PV_MUN_2035 ORDER BY nombre) LOOP',
'    APEX_JSON.OPEN_OBJECT;',
'    APEX_JSON.WRITE(''cod'', m.cod_ine); APEX_JSON.WRITE(''nombre'', m.nombre); APEX_JSON.WRITE(''pob'', m.poblacion);',
'    APEX_JSON.WRITE(''lat'', m.lat); APEX_JSON.WRITE(''lon'', m.lon); APEX_JSON.WRITE(''dist'', m.distancia_sol_km);',
'    APEX_JSON.WRITE(''tiempo'', m.tiempo_centro_min); APEX_JSON.WRITE(''modo'', m.modo); APEX_JSON.WRITE(''paradas'', m.paradas_total);',
'    APEX_JSON.WRITE(''escuelas'', m.escuelas); APEX_JSON.WRITE(''precio'', m.precio_medio); APEX_JSON.WRITE(''precio_m2'', m.precio_m2);',
'    APEX_JSON.WRITE(''compraventas'', m.compraventas); APEX_JSON.WRITE(''fiabilidad'', m.fiabilidad);',
'    APEX_JSON.WRITE(''dem'', m.dim_dem); APEX_JSON.WRITE(''viv'', m.dim_viv); APEX_JSON.WRITE(''ser'', m.dim_ser);',
'    APEX_JSON.WRITE(''acc'', m.dim_acc); APEX_JSON.WRITE(''emp'', m.dim_emp); APEX_JSON.WRITE(''indice'', m.indice);',
'    APEX_JSON.WRITE(''factor'', m.factor_limitante);',
'    APEX_JSON.WRITE(''p2035'', m.poblacion_2035); APEX_JSON.WRITE(''p10'', m.pob_2035_p10); APEX_JSON.WRITE(''p90'', m.pob_2035_p90);',
'    APEX_JSON.WRITE(''crec'', m.crecimiento_pct); APEX_JSON.WRITE(''esc'', m.escenario); APEX_JSON.WRITE(''fiabp'', m.fiab_pronostico);',
'    APEX_JSON.WRITE(''tasa'', m.tasa_2035_pct); APEX_JSON.WRITE(''conv'', m.pob_2035_convergencia); APEX_JSON.WRITE(''pers'', m.pob_2035_persistencia);',
'    APEX_JSON.WRITE(''san25'', m.hab_sanit_2025); APEX_JSON.WRITE(''san35'', m.hab_sanit_2035);',
'    APEX_JSON.WRITE(''edu25'', m.hab_escuela_2025); APEX_JSON.WRITE(''edu35'', m.hab_escuela_2035);',
'    APEX_JSON.WRITE(''par25'', m.hab_parada_2025); APEX_JSON.WRITE(''par35'', m.hab_parada_2035);',
'    APEX_JSON.WRITE(''viv25'', m.hab_vivienda_2025); APEX_JSON.WRITE(''viv35'', m.hab_vivienda_2035);',
'    APEX_JSON.OPEN_ARRAY(''serie'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''proy'');',
'    FOR s IN (SELECT poblacion FROM WKSP_DATATHON.PV_PROYECCION_SERIE WHERE cod_ine=m.cod_ine ORDER BY anio) LOOP APEX_JSON.WRITE(s.poblacion); END LOOP;',
'    APEX_JSON.CLOSE_ARRAY;',
'    APEX_JSON.OPEN_ARRAY(''vecinos'');',
'    FOR v IN (SELECT v.nombre_vecino, v.distancia_km, b.indice, b.factor_limitante, b.tiempo_centro_min',
'              FROM WKSP_DATATHON.PV_VECINOS v JOIN WKSP_DATATHON.PV_MUN_BASE b ON b.cod_ine=v.cod_vecino',
'              WHERE v.cod_ine=m.cod_ine ORDER BY v.distancia_km) LOOP',
'      APEX_JSON.OPEN_OBJECT; APEX_JSON.WRITE(''nombre'', v.nombre_vecino); APEX_JSON.WRITE(''dist'', v.distancia_km);',
'      APEX_JSON.WRITE(''indice'', v.indice); APEX_JSON.WRITE(''factor'', v.factor_limitante); APEX_JSON.WRITE(''tiempo'', v.tiempo_centro_min);',
'      APEX_JSON.CLOSE_OBJECT;',
'    END LOOP;',
'    APEX_JSON.CLOSE_ARRAY; APEX_JSON.CLOSE_OBJECT;',
'  END LOOP;',
'  APEX_JSON.CLOSE_ARRAY;',
'  v_json := APEX_JSON.GET_CLOB_OUTPUT; v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos)); v_pos := v_pos + 8000; END LOOP;',
'  APEX_JSON.FREE_OUTPUT;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>8900550584000018
);
end;
/
prompt --application/pages/page_00040
begin
wwv_flow_imp_page.create_page(
 p_id=>40
,p_name=>'Mapa'
,p_alias=>'MAPA'
,p_step_title=>'Mapa'
,p_autocomplete_on_off=>'OFF'
,p_step_template=>4073832297226169690
,p_page_template_options=>'#DEFAULT#'
,p_page_is_public_y_n=>'Y'
,p_protection_level=>'C'
,p_page_component_map=>'10'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(143622573347876360)
,p_plug_name=>'Mapa interactivo'
,p_static_id=>'mapa-interactivo'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4502917002193490937
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN',
'  -- 1. Estilos de la cabecera',
'  HTP.P(q''~<style>',
'.t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}',
'.t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}',
'.t-Header .a-Logo:hover{color:#5eead4!important}',
'</style>',
'~'');',
'',
'  -- 2. Mapa: estilos, HTML y JS',
'  HTP.P(q''~<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">',
'<style>',
'.mv{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto;padding:8px}',
'.mv .sub{font-size:13px;color:#5b6b7c;margin:0 0 10px}',
'.mv .topbar{display:flex;gap:14px;align-items:flex-end;margin:0 0 12px;flex-wrap:wrap}',
'.mv .topbar label{display:block;font-size:12px;font-weight:700;color:#334155;margin:0 0 4px}',
'.mv .topbar select{padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}',
'.mv .btnrun{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:10px 16px;font-weight:800;cursor:pointer;font-size:13px;height:38px}',
'.mv .btnrun:hover{filter:brightness(1.08)}',
'.mv .btnrun[disabled]{opacity:.6;cursor:wait}',
'.mv .bar{display:flex;gap:8px;align-items:flex-end;margin:0 0 0 auto;flex-wrap:wrap;opacity:.85}',
'.mv .bar label{display:block;font-size:11px;font-weight:700;color:#334155;margin:0 0 4px}',
'.mv .bar input,.mv .bar select{padding:6px 8px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;font-size:11px;background:#fff;max-width:130px}',
'.mv .bar .inerte{opacity:.55;pointer-events:none}',
'.mv .bar input[type=range]{max-width:110px}',
'.mv .err{display:none;margin:0 0 10px;font-size:12px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}',
'.mv .stage{position:relative;min-height:640px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;overflow:hidden}',
'.mv .stage.locked .mvBlur{filter:blur(7px);pointer-events:none;user-select:none}',
'.mv #mvOverlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(250,252,253,.72);color:#475569;font-weight:800;font-size:16px;z-index:60;text-align:center;padding:20px}',
'.mv #mvOverlay .spin{width:26px;height:26px;border-radius:50%;border:3px solid #cbd5e1;border-top-color:#0f766e;animation:mvspin .9s linear infinite}',
'@keyframes mvspin{to{transform:rotate(360deg)}}',
'.mv .grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:14px;align-items:start}',
'.mv #mvMap{height:640px;background:#d3d8dc;border-radius:10px;z-index:1}',
'.mv .side{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px;margin-bottom:12px}',
'.mv .side h4{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;margin:0 0 10px}',
'.mv .capa{display:block;font-size:12.5px;font-weight:600;color:#334155;margin:6px 0;cursor:pointer}',
'.mv .capa input{accent-color:#0f766e;margin-right:6px}',
'.mv .leg{height:10px;border-radius:5px;margin:8px 0 4px;background:linear-gradient(90deg,#C8102E,#f1f5f9 45%,#f1f5f9 55%,#1B7A3C)}',
'.mv .leg-et{display:flex;justify-content:space-between;font-size:11px;color:#64748b}',
'.mv .limchip{display:flex;align-items:center;gap:6px;font-size:12px;margin:5px 0}',
'.mv .limchip i{width:12px;height:12px;border-radius:50%;display:inline-block}',
'.mv .estado{font-size:11.5px;color:#64748b;line-height:1.5}',
'.mv .top{list-style:none;margin:0;padding:0;font-size:12px}',
'.mv .top li{display:flex;justify-content:space-between;gap:6px;padding:5px 6px;border-radius:7px;cursor:pointer}',
'.mv .top li:hover{background:#f4f7fa}',
'.mv .top li b{font-variant-numeric:tabular-nums}',
'.mv .tarjeta{position:absolute;top:12px;left:12px;width:300px;background:#fff;border:1px solid #dbe3ea;border-radius:12px;box-shadow:0 8px 22px rgba(15,42,68,.14);padding:12px;z-index:50;display:none;font-size:12px}',
'.mv .tarjeta b.t{font-size:15px;color:#0f2a44}',
'.mv .tarjeta .an{color:#64748b;font-size:11px;margin:2px 0 8px}',
'.mv .tarjeta .filas{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 0}',
'.mv .tarjeta .f{background:#f6f9fb;border-radius:8px;padding:6px 8px}',
'.mv .tarjeta .f div{font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:#5b6b7c;font-weight:700}',
'.mv .tarjeta .f b{font-size:13px;color:#0f2a44}',
'.mv .tarjeta .cierre{margin-top:8px;font-size:11px;color:#5b6b7c;border-top:1px dashed #e2e8f0;padding-top:6px}',
'.mv .pos{color:#0f766e}.mv .neg{color:#b91c1c}',
'.mv .pills{position:absolute;top:10px;right:10px;z-index:20;display:flex;gap:6px}',
'.mv .mv-pill{border:1px solid #cbd5e1;background:#fff;border-radius:99px;padding:5px 10px;font-size:11px;font-weight:700;cursor:pointer}',
'.mv .mv-pill.on{background:#0f766e;color:#fff;border-color:#0f766e}',
'.mv .ctx{position:fixed;z-index:99;background:#fff;border:1px solid #cbd5e1;border-radius:9px;box-shadow:0 8px 22px rgba(15,42,68,.14);display:none;min-width:140px;overflow:hidden}',
'.mv .ctx button{display:block;width:100%;text-align:left;background:#fff;border:0;padding:9px 12px;font:inherit;font-size:12px;font-weight:700;color:#334155;cursor:pointer}',
'.mv .ctx button:hover:enabled{background:#f4f7fa;color:#0f766e}',
'.mv .ctx button[disabled]{color:#94a3b8;cursor:not-allowed}',
'@media(max-width:1000px){.mv .grid{grid-template-columns:1fr}}',
'</style>',
'<div class="mv">',
' <div class="topbar">',
'  <div><label>A&ntilde;o: <span id="mvV">2030</span></label><input id="mvAnio" type="range" min="2025" max="2035" step="1" value="2030"></div>',
'  <div><button id="mvBtn" type="button" class="btnrun">Ejecutar Predicci&oacute;n</button></div>',
'  <div class="bar">',
'   <div><label>Buscar</label><input type="text" id="mvQ" disabled></div>',
'   <div><label>Comarca</label><select id="mvCom" disabled><option value="all">Todas</option></select></div>',
'   <div><label>Poblaci&oacute;n</label><input type="range" id="mvPop" disabled></div>',
'   <div><label>Transporte</label><input type="range" id="mvTr" disabled></div>',
'   <div><label>Cuello de botella</label><select id="mvLim" disabled>',
'     <option value="all">Cualquier factor</option>',
'     <option>Demogr&aacute;fico</option><option>Vivienda</option><option>Servicios</option>',
'     <option>Accesibilidad</option><option>Empleo</option>',
'   </select></div>',
'  </div>',
' </div>',
' <div id="mvErr" class="err"></div>',
' <div class="ctx" id="mvCtx" data-cod="">',
'  <button type="button" id="mvCtxDet">Detalles</button>',
'  <button type="button" id="mvCtxCmp" disabled title="Disponible pr&oacute;ximamente">Comparar</button>',
' </div>',
' <div class="stage locked" id="mvStage">',
'  <div id="mvOverlay"><div id="mvSpin" class="spin" style="display:none"></div><span id="mvOverlayTx">Ejecuta la predicci&oacute;n para visualizar</span></div>',
'  <div class="mvBlur">',
'   <div class="grid">',
'    <div style="position:relative"><div id="mvMap"></div>',
'     <div class="pills">',
'      <button type="button" id="mvSw" class="mv-pill" title="Alternar vista sat&eacute;lite / fondo plano">Sat&eacute;lite</button>',
'     </div>',
'    </div>',
'    <div class="lc-side">',
'     <div class="side"><h4>Capa activa (diferencial 2025 &rarr; a&ntilde;o)</h4><div id="mvCapas"></div><div id="mvLeyenda"></div></div>',
'     <div class="side"><h4>Estado</h4><div class="estado" id="mvEstado">&mdash;</div></div>',
'     <div class="side"><h4>Top 5</h4><ul class="top" id="mvTop"></ul></div>',
'    </div>',
'   </div>',
'   <div class="tarjeta" id="mvTarjeta"></div>',
'  </div>',
' </div>',
'</div>',
'<script>window.__MV_LIMITE = {"type":"Feature","geometry":{"type":"MultiPolygon","coordinates":[[[[-3.536705,41.160576],[-3.488751,41.094294],[-3.425805,41.082899],[-3.438935,41.04267],[-3.39445,41.000278],[-3.418296,40.987564],[-3.444062,40.906849],'
||'[-3.460577,40.906659],[-3.440487,40.87535],[-3.47257,40.864217],[-3.477387,40.823561],[-3.511572,40.788496],[-3.45901,40.781324],[-3.444343,40.76158],[-3.450416,40.734887],[-3.434945,40.727986],[-3.468553,40.689937],[-3.404735,40.669637],[-3.393354,4'
||'0.692458],[-3.345598,40.637743],[-3.316497,40.655177],[-3.338516,40.625849],[-3.321644,40.612192],[-3.328275,40.594836],[-3.284069,40.568977],[-3.297126,40.537521],[-3.249915,40.544316],[-3.199955,40.514449],[-3.198597,40.442252],[-3.155515,40.439425'
||'],[-3.130558,40.405185],[-3.15343,40.367703],[-3.141212,40.350542],[-3.182857,40.308267],[-3.194449,40.248037],[-3.173397,40.23417],[-3.153718,40.263714],[-3.112674,40.285478],[-3.101528,40.278092],[-3.067845,40.157914],[-3.089276,40.16297],[-3.09675'
||'5,40.142389],[-3.056194,40.113743],[-3.060707,40.090564],[-3.11819,40.061429],[-3.161579,40.064928],[-3.178137,40.092207],[-3.200956,40.060488],[-3.275756,40.047276],[-3.332241,40.080482],[-3.37529,40.075393],[-3.375783,40.051255],[-3.401072,40.03418'
||'1],[-3.506863,40.048674],[-3.519689,40.021072],[-3.589995,40.013172],[-3.637944,39.988352],[-3.634499,39.965892],[-3.74387,39.940802],[-3.804398,39.88472],[-3.868326,39.904859],[-3.87519,39.928736],[-3.840044,39.941956],[-3.832042,39.93156],[-3.80954'
||'8,39.953965],[-3.783347,39.944796],[-3.763602,39.967518],[-3.770486,39.950552],[-3.75437,39.950443],[-3.758817,39.968885],[-3.727936,39.964545],[-3.746207,39.981089],[-3.720088,39.984441],[-3.699891,40.019543],[-3.636088,40.041626],[-3.607628,40.1089'
||'67],[-3.655732,40.124912],[-3.667313,40.143291],[-3.683724,40.13227],[-3.722216,40.147713],[-3.744375,40.132224],[-3.770453,40.139399],[-3.804603,40.176841],[-3.834186,40.161353],[-3.872016,40.190153],[-3.931143,40.203977],[-3.950892,40.190335],[-3.9'
||'52866,40.212797],[-3.991002,40.209478],[-4.026159,40.235611],[-4.024028,40.248968],[-4.072894,40.265451],[-4.104272,40.241833],[-4.145769,40.245177],[-4.143992,40.264621],[-4.190871,40.297355],[-4.20323,40.268818],[-4.247999,40.273481],[-4.269961,40.'
||'235685],[-4.306111,40.221778],[-4.307989,40.233882],[-4.348488,40.236747],[-4.356386,40.308621],[-4.38011,40.318341],[-4.383482,40.289049],[-4.435246,40.259127],[-4.437426,40.236698],[-4.509789,40.21919],[-4.527911,40.200093],[-4.574993,40.206642],[-'
||'4.559329,40.231269],[-4.568788,40.258712],[-4.529379,40.293125],[-4.546225,40.341825],[-4.526788,40.344873],[-4.502898,40.314893],[-4.455762,40.319351],[-4.460596,40.341381],[-4.438636,40.352754],[-4.443729,40.3857],[-4.42173,40.406229],[-4.321089,40'
||'.410309],[-4.341252,40.428678],[-4.315679,40.464766],[-4.328218,40.533757],[-4.289262,40.564194],[-4.278572,40.603172],[-4.290709,40.627823],[-4.271102,40.629023],[-4.262141,40.60518],[-4.245439,40.602447],[-4.161183,40.623465],[-4.172853,40.630362],'
||'[-4.171567,40.680626],[-4.096991,40.747739],[-4.0767,40.788881],[-3.979676,40.784555],[-3.947105,40.862974],[-3.952276,40.893632],[-3.907197,40.955303],[-3.781366,41.000312],[-3.740455,41.05364],[-3.676065,41.086696],[-3.613703,41.149053],[-3.536705,'
||'41.160576]],[[-3.372259,40.635612],[-3.380257,40.632854],[-3.382135,40.630471],[-3.363665,40.631602],[-3.372259,40.635612]]],[[[-4.255731,40.65317],[-4.31951,40.647644],[-4.324122,40.658029],[-4.284817,40.681221],[-4.255731,40.65317]]]]},"properties"'
||':{"cod_ccaa":"13","noml_ccaa":"COMUNIDAD DE MADRID","name":"Madrid","cartodb_id":13,"created_at":"2014-09-30T00:00:00Z","updated_at":"2014-12-25T02:07:41Z"}};</script>',
'<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>',
'<script>',
'(function(){',
'"use strict";',
'var DATA=[], M={}, GEO=null, GEO_MUNS={}, RESULT=null, ANIO=2030, CAPA="difpob", SEL=null, READY=false;',
'var MAP=null, geoLayer=null, suelto=null, TILE=null;',
'var VERDE="#1B7A3C", ROJO="#C8102E", GRIS="#A0AEC0";',
'var COLOR_DIM={"Demograf\u00eda":"#7C3AED","Vivienda":"#B7791F","Servicios":"#0078A8","Accesibilidad":"#38A169","Empleo":"#D69E2E"};',
'var CAPAS=[',
'  {k:"difpob",  label:"\u0394Poblaci\u00f3n (hab.)",        f:function(m){return m.d_pob;},       dec:0},',
'  {k:"difpobp", label:"\u0394Poblaci\u00f3n (%)",           f:function(m){return m.d_pob_pct;},   dec:2},',
'  {k:"difidx",  label:"\u0394\u00cdndice de vitalidad",     f:function(m){return m.d_indice;},    dec:1},',
'  {k:"difval",  label:"\u0394Valor catastral (%)",          f:function(m){return m.d_valor_pct;}, dec:2},',
'  {k:"difsal",  label:"\u0394Salud (centros/10k)",          f:function(m){return num(m.salud_10k_y)-num(m.salud_10k_2025);}, dec:2},',
'  {k:"difesc",  label:"\u0394Escuelas (/1k)",               f:function(m){return num(m.escuelas_1000_y)-num(m.escuelas_1000_2025);}, dec:3},',
'  {k:"difpar",  label:"\u0394Paradas (/1k)",                f:function(m){return num(m.paradas_1000_y)-num(m.paradas_1000_2025);}, dec:3},',
'  {k:"difviv",  label:"\u0394Viviendas (/1k)",              f:function(m){return num(m.viv_1000_y)-num(m.viv_1000_2025);}, dec:1},',
'  {k:"lim",     label:"Factor limitante (a\u00f1o)",        f:function(m){return m.factor_limitante;}, dec:0}',
'];',
'function $(i){return document.getElementById(i);}',
'function esc(s){return (s==null?"":(""+s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}',
'function fmt(v,d){return (v===null||v===undefined)?"\u2014":Number(v).toLocaleString("es-ES",{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}',
'function num(v){v=Number(v);return isNaN(v)?0:v;}',
'function capaDef(k){for(var i=0;i<CAPAS.length;i++)if(CAPAS[i].k===k)return CAPAS[i];return CAPAS[0];}',
'function capaVal(m){try{var v=capaDef(CAPA).f(m);return (v==null||isNaN(v))?null:v;}catch(e){return null;}}',
'var MVMAX=1;',
'function calcularMax(){var mx=0;for(var i=0;i<DATA.length;i++){var v=capaVal(DATA[i]);if(v!==null&&v!==undefined)mx=Math.max(mx,Math.abs(num(v)));}MVMAX=mx||1;}',
'function colorCapa(m){',
'  if(CAPA==="lim")return COLOR_DIM[m.factor_limitante]||GRIS;',
'  var v=capaVal(m);if(v===null||v===undefined||num(v)===0)return GRIS;',
'  var t=Math.min(1,Math.abs(num(v))/MVMAX);',
'  var base=num(v)>0?[27,122,60]:[200,16,46];',
'  return "rgb("+Math.round(255-(255-base[0])*t)+","+Math.round(255-(255-base[1])*t)+","+Math.round(255-(255-base[2])*t)+")";',
'}',
'function api(n,p,cb){apex.server.process(n,p,{dataType:"json",success:cb,error:function(){var e=$("mvErr"),b=$("mvBtn"),s=$("mvSpin");if(e){e.style.display="block";e.textContent="El servidor respondio con error; revisa el log de la base.";}if(b)b.dis'
||'abled=false;if(s)s.style.display="none";var tx=document.getElementById("mvOverlayTx"),ov=document.getElementById("mvOverlay");if(tx){tx.textContent="Ejecuta la predicci\u00f3n para visualizar";}if(ov)ov.style.display="flex";}});}',
unistr('// \2500\2500 enlace Mapa \2192 Simulador What-If \2500\2500'),
unistr('// Guards selecci\00F3n en sessionStorage y navega a la p\00E1g. 10; ah\00ED el front del'),
'// Simulador, tras rellenar el select de municipios (DATOS), preseleciona el',
unistr('// municipio con el a\00F1o del mapa y ejecuta la FASE 1 (SIMULAR con sliders a 0).'),
'function abrirWI(cod,anio){',
'  if(!cod)return;',
'  try{sessionStorage.setItem("pvWiJugada",JSON.stringify({cod:String(cod),anio:Number(anio)||2030}));}catch(e){}',
'  apex.navigation.redirect("f?p="+apex.env.APP_ID+":10:"+apex.env.APP_SESSION+"::NO:::");',
'}',
'function menuCtx(x,y,cod){',
'  var m=$("mvCtx");if(!m)return;',
'  if(!cod){m.style.display="none";return;}',
'  m.setAttribute("data-cod",String(cod));',
'  m.style.right="";m.style.bottom="";',
'  m.style.display="block";',
'  var w=m.offsetWidth||140,h=m.offsetHeight||84;',
'  m.style.left=Math.max(6,Math.min(x,window.innerWidth-w-6))+"px";',
'  m.style.top=Math.max(6,Math.min(y,window.innerHeight-h-6))+"px";',
'}',
'function cerrarCtx(){var m=$("mvCtx");if(m)m.style.display="none";}',
'function render(){',
'  calcularMax();',
'  if(geoLayer)geoLayer.eachLayer(function(l){l.setStyle({fillColor:colorCapa(M[l.__cod]||{})});});',
'  if(suelto)suelto.eachLayer(function(l){l.setStyle({fillColor:colorCapa(M[l.__cod]||{})});});',
'  dibujarTop();dibujarLeyenda();dibujarEstado();if(SEL&&M[SEL])pintarTarjeta(M[SEL],true);',
'}',
'function dibujarTop(){',
'  var clave=(CAPA==="lim")?"d_indice":CAPA;',
'  var lista=DATA.slice().sort(function(a,b){return num(b[clave==="difpob"?"d_pob":clave])-num(a[clave==="difpob"?"d_pob":clave]);}).slice(0,5);',
'  var def=capaDef(CAPA);',
'  $("mvTop").innerHTML=lista.map(function(m,i){return "<li data-cod=\""+m.cod+"\"><span><b>"+(i+1)+".</b> "+esc(m.nombre)+"</span><b>"+(CAPA==="lim"?esc(m.factor_limitante):fmt(capaVal(m),def.dec))+"</b></li>";}).join("");',
'  Array.prototype.forEach.call($("mvTop").querySelectorAll("li"),function(li){li.onclick=function(){SEL=li.getAttribute("data-cod");if(M[SEL])pintarTarjeta(M[SEL],true);};});',
'}',
'function dibujarLeyenda(){',
'  var el=$("mvLeyenda");',
'  if(CAPA==="lim"){el.innerHTML=Object.keys(COLOR_DIM).map(function(d){return "<div class=\"limchip\"><i style=\"background:"+COLOR_DIM[d]+"\"></i>"+esc(d)+"</div>";}).join("");return;}',
'  var mx=MVMAX||1;var dec=capaDef(CAPA).dec;',
'  el.innerHTML="<div class=\"leg\"></div><div class=\"leg-et\"><span class=\"neg\">\u25BC "+fmt(-mx,dec)+"</span><span>0</span><span class=\"pos\">\u25B1 +"+fmt(mx,dec)+"</span></div>";',
'}',
'function dibujarEstado(){$("mvEstado").innerHTML="Mostrando <b>"+DATA.length+"</b> municipios \u00B7 A\u00F1o <b>"+ANIO+"</b><br>Modelos: M1 + M2 (\u00D75) + M3 + M4 \u00B7 ONNX dentro de Oracle";}',
'function pintarTarjeta(m,fij){',
'  var c=capaDef(CAPA);var v=capaVal(m);var col=(num(v)>0)?"pos":(num(v)<0)?"neg":"";',
'  var cuerpo=(CAPA==="lim")',
'    ? "<div class=\"f\" style=\"grid-column:1/-1\"><div>Factor limitante "+ANIO+"</div><b>"+esc(m.factor_limitante)+"</b></div>"',
'    : "<div class=\"f\" style=\"grid-column:1/-1\"><div>"+esc(c.label)+"</div><b class=\""+col+"\">"+(num(v)>0?"+":"")+fmt(v,c.dec)+"</b></div>";',
'  var filas=[',
'    ["Poblaci\u00f3n",fmt(m.pob_2025)+" \u2192 "+fmt(m.pob_y)],',
'    ["\u0394Poblaci\u00f3n",(m.d_pob>0?"+":"")+fmt(m.d_pob)+" ("+fmt(m.d_pob_pct,2)+"%)"],',
'    ["\u00CDndice",fmt(m.indice_2025,1)+" \u2192 "+fmt(m.indice_y,1)],',
'    ["Banda M1",fmt(m.p10)+" / "+fmt(m.p90)],',
'    ["Salud/10k",fmt(m.salud_10k_2025,2)+" \u2192 "+fmt(m.salud_10k_y,2)],',
'    ["Escuelas/1k",fmt(m.escuelas_1000_2025,3)+" \u2192 "+fmt(m.escuelas_1000_y,3)],',
'    ["Paradas/1k",fmt(m.paradas_1000_2025,3)+" \u2192 "+fmt(m.paradas_1000_y,3)],',
'    ["Viviendas/1k",fmt(m.viv_1000_2025,1)+" \u2192 "+fmt(m.viv_1000_y,1)],',
'    ["Valor catastral",fmt(m.valor_2025)+" \u2192 "+fmt(m.valor_y)+" \u20AC"],',
'    ["\u0394Valor",fmt(m.d_valor_pct,2)+" %"]',
'  ];',
'  var grid=filas.map(function(x){return "<div class=\"f\"><div>"+x[0]+"</div><b>"+x[1]+"</b></div>";}).join("");',
'  $("mvTarjeta").innerHTML="<b class=\"t\">"+esc(m.nombre)+"</b><div class=\"an\">cod "+m.cod+" \u00B7 a\u00F1o "+ANIO+" \u00B7 base 2025</div>"',
'   +"<div class=\"filas\">"+cuerpo+grid+"</div>"',
'   +"<div class=\"cierre\">Factor limitante: <b>"+esc(m.factor_limitante)+"</b> \u00B7 M1+M2+M3+M4 ONNX en Oracle \u00B7 salida ef\u00EDmera</div>";',
'  $("mvTarjeta").style.display="block";',
'}',
'function cerrarTarjeta(){$("mvTarjeta").style.display="none";}',
'function run(){',
'  if($("mvBtn").disabled)return;',
'  $("mvErr").style.display="none";',
'  $("mvBtn").disabled=true;$("mvSpin").style.display="block";$("mvOverlayTx").textContent="Cargando\u2026";$("mvOverlay").style.display="flex";',
'  ANIO=Number($("mvAnio").value)||2030;$("mvV").textContent=String(ANIO);',
'  api("PRED",{x01:ANIO},function(d){',
'   $("mvBtn").disabled=false;$("mvSpin").style.display="none";',
'   RESULT=d;DATA=d.municipios||[];M={};DATA.forEach(function(m){M[m.cod]=m;});',
'   $("mvStage").classList.remove("locked");$("mvOverlay").style.display="none";',
'   calcularMax();render();',
'  });',
'}',
'function pintaGeo(){',
'  if(geoLayer)MAP.removeLayer(geoLayer);',
'  geoLayer=L.geoJSON(GEO,{',
'    style:function(f){return {color:"#fff",weight:1,fillColor:colorCapa(M[f.properties.cod]||{}),fillOpacity:.85};},',
'    onEachFeature:function(f,l){l.__cod=f.properties.cod;',
'     l.on("mouseover",function(){l.setStyle({weight:2.5,color:"#232323"});if(M[f.properties.cod])pintarTarjeta(M[f.properties.cod],false);});',
'     l.on("mouseout",function(){l.setStyle({weight:1,color:"#fff"});if(SEL!==f.properties.cod)cerrarTarjeta();});',
'     l.on("click",function(){ if(M[f.properties.cod]){ cerrarCtx(); abrirWI(f.properties.cod,$("mvAnio").value); } });',
'     l.on("contextmenu",function(ev){',
'       var oe=ev.originalEvent;',
'       if(oe&&oe.preventDefault){oe.preventDefault();}',
'       if(oe&&oe.stopPropagation){oe.stopPropagation();}',
'       menuCtx((oe&&oe.clientX)||0,(oe&&oe.clientY)||0,f.properties.cod);',
'     });',
'    }',
'  }).addTo(MAP);',
'}',
'function dibujarSueltos(){',
'  if(!suelto)return;suelto.clearLayers();',
'  DATA.forEach(function(m){ if(GEO_MUNS[m.cod])return;',
'   var mk=L.circleMarker([m.lat,m.lon],{radius:7,fillColor:colorCapa(m),fillOpacity:.85,color:"#fff",weight:1.5});',
'   mk.__cod=m.cod;',
'   mk.on("click",function(){cerrarCtx();abrirWI(m.cod,$("mvAnio").value);});',
'   mk.on("contextmenu",function(ev){var oe=ev.originalEvent;if(oe&&oe.preventDefault)oe.preventDefault();menuCtx((oe&&oe.clientX)||0,(oe&&oe.clientY)||0,m.cod);});',
'   mk.on("mouseover",function(){pintarTarjeta(m,false);});',
'   mk.on("mouseout",function(){if(SEL!==m.cod)cerrarTarjeta();});',
'   suelto.addLayer(mk);',
'  });',
'}',
'',
'function boot(){',
'  MAP=L.map("mvMap",{center:[40.55,-3.65],zoom:9,minZoom:8,maxZoom:13,zoomControl:false});',
'  L.control.zoom({position:"bottomright"}).addTo(MAP);',
'  MAP.on("click",function(){SEL=null;cerrarTarjeta();});',
'  MAP.on("contextmenu",function(){cerrarCtx();});',
'  var bd=$("mvCtxDet");if(bd)bd.addEventListener("click",function(){var m=$("mvCtx");var c=m?m.getAttribute("data-cod"):null;cerrarCtx();abrirWI(c,$("mvAnio").value);});',
unistr('  var bc=$("mvCtxCmp");if(bc)bc.addEventListener("click",function(){ /* Comparar: no implementado todav\00EDa */ });'),
'  document.addEventListener("click",cerrarCtx);',
'  document.addEventListener("contextmenu",function(ev){ if(ev.target && ev.target.closest && ev.target.closest("#mvCtx")) return; cerrarCtx(); });',
unistr('  // Fondo: gris plano por defecto; el interruptor "Sat\00E9lite" alterna la capa satelital'),
'  var TILES={',
'   sat:{url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",opt:{maxZoom:19,attribution:"Tiles \u00A9 Esri, Maxar"}}',
'  };',
'  function setTile(k){',
'   if(TILE){MAP.removeLayer(TILE);TILE=null;}',
'   if(k&&TILES[k]){TILE=L.tileLayer(TILES[k].url,TILES[k].opt).addTo(MAP);TILE.bringToBack();}',
'   var b=$("mvSw");if(b)b.classList.toggle("on",!!TILE);',
'  }',
'  var bsw=$("mvSw");if(bsw)bsw.addEventListener("click",function(){setTile(TILE?null:"sat");});',
'  L.geoJSON(window.__MV_LIMITE,{style:{color:"#0078A8",weight:2,dashArray:"3, 4",fillColor:"#0078A8",fillOpacity:0.04},interactive:false}).addTo(MAP);',
'  suelto=L.layerGroup().addTo(MAP);',
'  $("mvCapas").innerHTML=CAPAS.map(function(c){return "<label class=\"capa"+(c.k===CAPA?" on":"")+"\"><input type=\"radio\" name=\"mvcapa\" value=\""+c.k+"\""+(c.k===CAPA?" checked":"")+">"+esc(c.label)+"</label>";}).join("");',
'  Array.prototype.forEach.call(document.querySelectorAll(''input[name=mvcapa]''),function(r){r.addEventListener("change",function(){CAPA=r.value;render();});});',
'  window.addEventListener("resize",function(){MAP.invalidateSize();});',
'  api("GEO",{},function(fc){GEO=fc;GEO_MUNS={};(fc.features||[]).forEach(function(f){GEO_MUNS[f.properties.cod]=true;});pintaGeo();dibujarSueltos();render();});',
'  setTimeout(function(){MAP.invalidateSize();},300);',
'  READY=true;',
'}',
unistr('// \2500\2500 listeners b\00E1sicos (sin Leaflet) \2500\2500'),
'$("mvAnio").addEventListener("input",function(){$("mvV").textContent=this.value;});',
'$("mvBtn").addEventListener("click",function(){ if(READY)run(); });',
'document.addEventListener("keydown",function(e){ if(e.key==="Enter"&&READY&&!$("mvBtn").disabled){ e.preventDefault(); run(); } });',
unistr('// \2500\2500 arranque: espera Leaflet + apex, luego boot \2500\2500'),
'var _intentos=0;',
'(function _w(){ _intentos++;',
' if(_intentos>300)return;',
' if(window.apex&&window.apex.server&&window.L&&window.__MV_LIMITE){setTimeout(boot,150);} else {setTimeout(_w,100);}',
'})();',
'})();',
'</script>~'');',
'END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(143622573347876362)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'GEO'
,p_static_id=>'geo'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_arr CLOB;',
'  v_json CLOB;',
'  v_len PLS_INTEGER;',
'  v_pos PLS_INTEGER := 1;',
'BEGIN',
'  SELECT JSON_ARRAYAGG(',
'    JSON_OBJECT(''type'' VALUE ''Feature'',',
'      ''geometry'' VALUE JSON(g.GEO),',
'      ''properties'' VALUE JSON_OBJECT(''cod'' VALUE g.COD_INE, ''nombre'' VALUE g.NOMBRE RETURNING CLOB)',
'      RETURNING CLOB) RETURNING CLOB)',
'  INTO v_arr FROM PV_GEO_MUNIS g;',
'  v_json := ''{"type":"FeatureCollection","features":'' || v_arr || ''}'';',
'  v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP',
'    HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos));',
'    v_pos := v_pos + 8000;',
'  END LOOP;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>19247586701514294
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(143622573347876361)
,p_process_sequence=>10
,p_process_point=>'ON_DEMAND'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'PRED'
,p_static_id=>'pred'
,p_process_sql_clob=>wwv_flow_string.join(wwv_flow_t_varchar2(
'DECLARE',
'  v_json CLOB;',
'  v_len PLS_INTEGER;',
'  v_pos PLS_INTEGER := 1;',
'BEGIN',
'  v_json := WKSP_DATATHON.PV_MAPA(TO_NUMBER(apex_application.g_x01));',
'  v_len := DBMS_LOB.GETLENGTH(v_json);',
'  WHILE v_pos <= v_len LOOP',
'    HTP.PRN(DBMS_LOB.SUBSTR(v_json, 8000, v_pos));',
'    v_pos := v_pos + 8000;',
'  END LOOP;',
'END;'))
,p_process_clob_language=>'PLSQL'
,p_internal_uid=>19247586701514293
);
end;
/
prompt --application/deployment/definition
begin
wwv_flow_imp.g_varchar2_table := wwv_flow_imp.empty_varchar2_table;
wwv_flow_imp_shared.create_install(
 p_id=>wwv_flow_imp.id(144959777037110937)
,p_deinstall_script_clob=>wwv_flow_imp.varchar2_to_clob(wwv_flow_imp.g_varchar2_table)
);
end;
/
prompt --application/deployment/checks
begin
null;
end;
/
prompt --application/deployment/buildoptions
begin
null;
end;
/
prompt --application/end_environment
begin
wwv_flow_imp.import_end(p_auto_install_sup_obj => nvl(wwv_flow_application_install.get_auto_install_sup_obj, false)
);
commit;
end;
/
set verify on feedback on define on
prompt  ...done
