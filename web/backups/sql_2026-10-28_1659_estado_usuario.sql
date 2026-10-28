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
,p_default_id_offset=>0
,p_default_owner=>'WKSP_DATATHON'
);
end;
/
 
prompt APPLICATION 215 - Pueblos con Vida
--
-- Application Export:
--   Application:     215
--   Name:            Pueblos con Vida
--   Exported By:     ADMIN
--   Flashback:       0
--   Export Type:     Application Export
--     Pages:                      4
--       Processes:                4
--       Regions:                  4
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
,p_authentication_id=>wwv_flow_imp.id(8900550584000001)
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
,p_version_scn=>'51011739381168'
,p_print_server_type=>'INSTANCE'
,p_file_storage=>'DB'
,p_is_pwa=>'N'
,p_theme_id=>42
,p_home_url=>'f?p=&APP_ID.:1:&APP_SESSION.::&DEBUG.:::'
,p_login_url=>'f?p=&APP_ID.:101:&APP_SESSION.::&DEBUG.:::'
,p_theme_style_by_user_pref=>false
,p_built_with_love=>false
,p_navigation_list_id=>wwv_flow_imp.id(8900550584000004)
,p_navigation_list_position=>'SIDE'
,p_navigation_list_template_id=>2469215554099805162
,p_nav_list_template_options=>'#DEFAULT#:js-defaultCollapsed:js-navCollapsed--hidden:t-TreeNav--styleA'
,p_nav_bar_type=>'LIST'
,p_nav_bar_list_id=>wwv_flow_imp.id(8900550584000005)
,p_nav_bar_list_template_id=>2849019392706229583
,p_nav_bar_template_options=>'#DEFAULT#'
);
end;
/
prompt --application/plugin_settings
begin
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235482427095855)
,p_plugin_type=>'DYNAMIC ACTION'
,p_plugin=>'NATIVE_OPEN_AI_ASSISTANT'
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235725621095856)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_COLOR_PICKER'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_as', 'POPUP',
  'mode', 'FULL')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235860659095856)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_DATE_PICKER_APEX'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'appearance_behavior', 'MONTH-PICKER:YEAR-PICKER:TODAY-BUTTON',
  'days_outside_month', 'VISIBLE',
  'show_on', 'FOCUS',
  'time_increment', '15')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235649897095856)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_GEOCODED_ADDRESS'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'background', 'default',
  'display_as', 'LIST',
  'map_preview', 'POPUP:ITEM',
  'match_mode', 'RELAX_HOUSE_NUMBER')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236190586095857)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_SELECT_MANY'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_values_as', 'separated')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235530645095855)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_SINGLE_CHECKBOX'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'checked_value', 'Y',
  'unchecked_value', 'N')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10235935077095857)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_STAR_RATING'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'default_icon', 'fa-star',
  'tooltip', '#VALUE#')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236091027095857)
,p_plugin_type=>'ITEM TYPE'
,p_plugin=>'NATIVE_YES_NO'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'display_style', 'SWITCH_CB',
  'off_value', 'N',
  'on_value', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236216919095858)
,p_plugin_type=>'PROCESS TYPE'
,p_plugin=>'NATIVE_GEOCODING'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'match_mode', 'RELAX_HOUSE_NUMBER')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236451679095858)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_DISPLAY_SELECTOR'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'include_slider', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236572738095859)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_IR'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'actions_menu_structure', 'IG')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236336022095858)
,p_plugin_type=>'REGION TYPE'
,p_plugin=>'NATIVE_MAP_REGION'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'use_vector_tile_layers', 'Y')).to_clob
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236628210095859)
,p_plugin_type=>'WEB SOURCE TYPE'
,p_plugin=>'NATIVE_ADFBC'
);
wwv_flow_imp_shared.create_plugin_setting(
 p_id=>wwv_flow_imp.id(10236784071095859)
,p_plugin_type=>'WEB SOURCE TYPE'
,p_plugin=>'NATIVE_BOSS'
);
end;
/
prompt --application/shared_components/navigation/lists/navigation_bar
begin
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(8900550584000005)
,p_name=>'Navigation Bar'
,p_static_id=>'navigation-bar'
,p_version_scn=>'1'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000006)
,p_list_item_display_sequence=>10
,p_list_item_link_text=>'&APP_USER.'
,p_static_id=>'app-user'
,p_list_item_link_target=>'#'
,p_list_item_icon=>'fa-user'
,p_list_item_current_type=>'NEVER'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000007)
,p_list_item_display_sequence=>20
,p_list_item_link_text=>'Logout'
,p_static_id=>'logout'
,p_list_item_link_target=>'&LOGOUT_URL.'
,p_list_item_icon=>'fa-sign-out'
,p_parent_list_item_id=>wwv_flow_imp.id(8900550584000006)
,p_list_item_current_type=>'NEVER'
);
end;
/
prompt --application/shared_components/navigation/lists/navigation_menu
begin
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(8900550584000004)
,p_name=>'Navigation Menu'
,p_static_id=>'navigation-menu'
,p_version_scn=>'1'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000022)
,p_list_item_display_sequence=>40
,p_list_item_link_text=>'Datos'
,p_static_id=>'datos'
,p_list_item_link_target=>'f?p=&APP_ID.:30:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'TARGET_PAGE'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(8900550584000020)
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
 p_id=>wwv_flow_imp.id(8900550584000003)
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
 p_id=>wwv_flow_imp.id(8900550584000001)
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
 p_id=>wwv_flow_imp.id(8900550584000009)
,p_plug_name=>'Portada'
,p_static_id=>'portada'
,p_region_template_options=>'#DEFAULT#'
,p_plug_template=>4073835273271169698
,p_plug_display_sequence=>10
,p_plug_item_display_point=>'ABOVE'
,p_location=>null
,p_plug_source=>wwv_flow_string.join(wwv_flow_t_varchar2(
'BEGIN HTP.P(q''~<style>',
'.pvh{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;max-width:1100px;margin:0 auto;color:#0f172a}',
'.pvh .hero{background:linear-gradient(135deg,#0f2a44,#163a5c);color:#fff;border-radius:18px;padding:34px 34px 30px;margin:8px 0 20px}',
'.pvh .kick{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#9fd8d0;font-weight:800}',
'.pvh h1{font-size:36px;line-height:1.1;margin:8px 0 8px;letter-spacing:-.02em}',
'.pvh .sub{color:#cfe0ee;font-size:15px;max-width:760px;line-height:1.5;margin:0}',
'.pvh .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}',
'.pvh .card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #dbe3ea;border-radius:16px;padding:22px;box-shadow:0 1px 2px rgba(15,42,68,.05),0 8px 22px rgba(15,42,68,.07);transition:transform .15s,box-shadow .15s}',
'.pvh .card:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(15,42,68,.12)}',
'.pvh .ico{width:42px;height:42px;border-radius:12px;background:#eefaf8;color:#0f766e;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;margin-bottom:12px}',
'.pvh h2{font-size:19px;margin:0 0 6px;color:#0f2a44}',
'.pvh p{font-size:13px;color:#5b6b7c;line-height:1.5;margin:0 0 10px}',
'.pvh .go{font-size:12px;font-weight:800;color:#0f766e}',
'.pvh .foot{font-size:11px;color:#64748b;margin:16px 0 4px;line-height:1.5}',
'@media(max-width:800px){.pvh .cards{grid-template-columns:1fr}.pvh h1{font-size:28px}.pvh .hero{padding:24px}}',
'</style>',
'<div class="pvh">',
'  <div class="hero">',
unistr('    <div class="kick">II Datathon LoDCOREMadrid \00B7 2026</div>'),
'    <h1>Pueblos con Vida</h1>',
unistr('    <p class="sub">155 municipios de menos de 50.000 habitantes, datos abiertos 2010-2025, proyecci\00F3n a 2035 y un simulador para decidir d\00F3nde puede crecer la Comunidad de Madrid.</p>'),
'  </div>',
'  <div class="cards">',
'    <a class="card" href="#" data-page="10">',
unistr('      <div class="ico">\D83C\DFDB</div><h2>Perfil institucional</h2>'),
unistr('      <p>Simula nuevos residentes, vivienda, sanidad, escuelas y transporte. Ve el efecto en el \00EDndice, en los ratios por habitante, en los vecinos y en la proyecci\00F3n 2035.</p>'),
unistr('      <div class="go">Abrir simulador \2192</div>'),
'    </a>',
'    <a class="card" href="#" data-page="20">',
unistr('      <div class="ico">\D83C\DFE1</div><h2>Perfil ciudadano</h2>'),
unistr('      <p>Elige tiempo a Madrid, precio, servicios y empleo. Obt\00E9n un ranking explicado, mapa de afinidad y ficha con la poblaci\00F3n proyectada a 2035.</p>'),
unistr('      <div class="go">Buscar mi municipio \2192</div>'),
'    </a>',
'    <a class="card" href="#" data-page="30">',
unistr('      <div class="ico">\D83D\DCCA</div><h2>Datos abiertos</h2>'),
unistr('      <p>Consulta las tablas completas de los 155 municipios: indicadores, proyecci\00F3n 2035, banda de incertidumbre y presi\00F3n sobre servicios. Descarga en CSV.</p>'),
unistr('      <div class="go">Ver las tablas \2192</div>'),
'    </a>',
'  </div>',
unistr('  <div class="foot">Fuentes: Comunidad de Madrid, INE, IGN y CRTM. Precios de escritura: Notariado v\00EDa S\00F3kerim (CC-BY 4.0). Licencia de salida CC-BY. Atribuci\00F3n CRTM: Powered by CRTM. Los huecos son NA: no se imputan.</div>'),
'</div>',
'<script>',
'document.querySelectorAll(''[data-page]'').forEach(function(a){a.addEventListener(''click'',function(e){e.preventDefault();location.href=''f?p=''+apex.env.APP_ID+'':''+a.getAttribute(''data-page'')+'':''+apex.env.APP_SESSION;});});',
'</script>~''); END;'))
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
 p_id=>wwv_flow_imp.id(8900550584000013)
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
'.t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}',
'.t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}',
'.t-Header .a-Logo:hover{color:#5eead4!important}',
'</style>',
'</style>~'');',
'',
'  -- 2. Estilos, HTML y JS del simulador (prediccion + what-if)',
'  HTP.P(q''~<style>',
'.sw{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1280px;margin:0 auto;padding:8px}',
'.sw .bar{display:flex;gap:8px;align-items:center;margin:0 0 0 auto}',
'.sw .dldrop{position:relative;margin-left:auto;display:flex;gap:8px;align-items:center}',
'.sw .dlmenu{display:none;position:absolute;right:0;top:calc(100% + 4px);background:#fff;border:1px solid #cbd5e1;border-radius:9px;box-shadow:0 8px 22px rgba(15,42,68,.14);z-index:20;min-width:150px;overflow:hidden}',
'.sw .dlmenu button{display:block;width:100%;text-align:left;background:#fff;border:0;padding:9px 12px;font:inherit;font-size:12px;font-weight:700;color:#334155;cursor:pointer}',
'.sw .dlmenu button:hover{background:#f4f7fa;color:#0f766e}',
'.sw .btn2{background:#fff;border:1px solid #cbd5e1;color:#0f766e;font-weight:800;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:12px}',
'.sw .btn2:hover{filter:brightness(1.05)}',
'.sw .btn2[disabled]{opacity:.45;cursor:not-allowed}',
'.sw h1{font-size:26px;line-height:1.15;margin:6px 0 2px;color:#0f2a44}',
'.sw .sub{font-size:13px;color:#5b6b7c;margin:0 0 8px}',
'.sw .topbar{display:flex;gap:12px;align-items:flex-end;margin:0 0 16px;flex-wrap:wrap}',
'.sw .topbar>div:not(.dldrop){min-width:200px}',
'.sw .topbar label{margin:0 0 4px}',
'.sw .btnrun{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:10px 16px;font-weight:800;cursor:pointer;font-size:13px;height:38px}',
'.sw .btnrun:hover{filter:brightness(1.08)}',
'.sw .btnrun[disabled]{opacity:.6;cursor:wait}',
'.sw .wrap{display:grid;grid-template-columns:300px minmax(0,1fr);gap:16px;align-items:start}',
'.sw .panel{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;position:sticky;top:12px}',
'.sw .panel h2{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#5b6b7c;margin:0 0 12px}',
'.sw label{display:block;font-size:12px;font-weight:700;color:#334155;margin:10px 0 4px}',
'.sw input,.sw select{width:100%;padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}',
'.sw input[type=number]{font-variant-numeric:tabular-nums}',
'.sw input[disabled],.sw select[disabled]{background:#f4f7fa;color:#94a3b8}',
'.sw .note{font-size:11px;color:#5b6b7c;line-height:1.45;margin-top:12px;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px}',
'.sw .err{display:none;margin-top:10px;font-size:12px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}',
'.sw .stage{position:relative;min-height:560px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;overflow:hidden}',
'.sw .stage.locked #swRes{filter:blur(7px);pointer-events:none;user-select:none}',
'.sw #swOverlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(250,252,253,.72);color:#475569;font-weight:800;font-size:16px;z-index:5;text-align:center;padding:20px}',
'.sw #swOverlay .spin{width:26px;height:26px;border-radius:50%;border:3px solid #cbd5e1;border-top-color:#0f766e;animation:swspin .9s linear infinite}',
'@keyframes swspin{to{transform:rotate(360deg)}}',
'.sw .kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:14px}',
'.sw .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px}',
'.sw .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}',
'.sw .kpi b{display:block;font-size:24px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}',
'.sw .kpi .s{font-size:11px;color:#5b6b7c}',
'.sw .card{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:14px;margin-bottom:12px}',
'.sw h3{font-size:13px;margin:0 0 10px;color:#0f2a44}',
'.sw .dim{display:grid;grid-template-columns:96px 1fr 1fr 84px;gap:7px;align-items:center;font-size:11px;margin:8px 0}',
'.sw .dim span{font-weight:700;color:#334155}',
'.sw .track{height:8px;background:#eef2f6;border-radius:99px;overflow:hidden}',
'.sw .track i{display:block;height:100%;border-radius:99px}',
'.sw .track .before{background:#cbd5e1}.sw .track .after{background:#14b8a6}',
'.sw .dim b{text-align:right;font-variant-numeric:tabular-nums;color:#0f2a44}',
'.sw table{width:100%;border-collapse:collapse;font-size:12px}',
'.sw th{text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea}',
'.sw td{padding:6px;border-bottom:1px solid #eef2f6}',
'.sw .num{text-align:right;font-variant-numeric:tabular-nums}',
'.sw label .difval{float:right;font-variant-numeric:tabular-nums;font-weight:800}',
'.sw .difval.pos{color:#0f766e}.sw .difval.neg{color:#b91c1c}.sw .difval.zero{color:#94a3b8}',
'.sw input[type=range]{accent-color:#0f766e;padding:0}',
'@media(max-width:980px){.sw .wrap,.sw .kpis{grid-template-columns:1fr}.sw .panel{position:static}}',
'</style>',
'<div class="sw">',
'<h1>Simulador What-If</h1>',
' <div class="topbar">',
'  <div><label>Municipio</label><select id="swCod"></select></div>',
'  <div><label>A&ntilde;o de predicci&oacute;n</label><select id="swAnio"></select></div>',
'  <div><button id="swBtn" type="button" class="btnrun">Ejecutar Simulaci&oacute;n</button></div>',
'  <div class="dldrop">',
'   <button id="swBtnDl" type="button" class="btn2" disabled>Descargar</button>',
'   <button id="swBtnImp" type="button" class="btn2">Importar JSON</button>',
'   <div class="dlmenu" id="swDlMenu" style="display:none">',
'    <button type="button" data-fmt="json">JSON (.json)</button>',
'    <button type="button" data-fmt="csv">CSV (.csv)</button>',
'   </div>',
'   <input id="swFile" type="file" accept=".json,application/json" style="display:none">',
'  </div>',
' </div>',
' <div class="wrap">',
'  <div class="panel">',
'   <h2>Diferenciales del escenario (What-If)</h2>',
'   <label>Diferencial de residentes <span id="swPopV" class="difval zero">0</span></label>',
'   <input id="swPop" type="range" step="1" value="0" disabled>',
'   <label>Diferencial de viviendas <span id="swVivV" class="difval zero">0</span></label>',
'   <input id="swViv" type="range" step="1" value="0" disabled>',
'   <label>Diferencial de centros de salud <span id="swSalV" class="difval zero">0</span></label>',
'   <input id="swSal" type="range" step="1" value="0" disabled>',
'   <label>Diferencial de escuelas <span id="swEscV" class="difval zero">0</span></label>',
'   <input id="swEsc" type="range" step="1" value="0" disabled>',
'   <label>Diferencial de paradas <span id="swParV" class="difval zero">0</span></label>',
'   <input id="swPar" type="range" step="1" value="0" disabled>',
'   <div id="swErr" class="err"></div>',
unistr('   <div class="note">Se emplean los modelos <b>M3</b> (proyeccion base al a\00F1o seleccionado) y <b>M4</b> (Suma de diferenciales y 5 dimensiones)</div>'),
'  </div>',
'  <div class="stage locked" id="swStage">',
'   <div id="swOverlay"><span id="swSpin" class="spin" style="display:none"></span>Ejecuta la simulaci&oacute;n para visualizar</div>',
'   <div id="swRes" style="padding:16px">',
'    <div class="kpis">',
'     <div class="kpi"><div class="l">&Iacute;ndice antes &rarr; escenario</div><b><span id="swIdxA">--</span> &rarr; <span id="swIdxB">--</span></b><div class="s"><span id="swDelta"></span> <span id="swLimit" style="color:#64748b"></span></div></div>',
'     <div class="kpi"><div class="l">Poblaci&oacute;n proyectada M3</div><b id="swPobBase">--</b><div class="s">banda <span id="swBand">--</span> &middot; factor <span id="swFactor">--</span></div></div>',
'     <div class="kpi"><div class="l">Poblaci&oacute;n escenario</div><b id="swPob">--</b><div class="s" id="swPobS"></div></div>',
'    </div>',
'    <div class="card">',
'     <h3>Cinco dimensiones (0-100)</h3>',
'     <div id="swDims"></div>',
'    </div>',
'    <div class="card">',
'     <h3>Ratios de saturaci&oacute;n</h3>',
'     <table id="swRatios"></table>',
'    </div>',
'    <div class="card">',
'     <h3>Choque aplicado</h3>',
'     <table id="swChoques"></table>',
'    </div>',
'   </div>',
'  </div>',
' </div>',
'</div>',
'<script>',
'(function(){',
' var RESULT=null, BASE=false;',
' function $(i){return document.getElementById(i);}',
' function esc(s){return (s==null?"":(""+s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}',
' function num(v,d){return (v==null||v==="")?"--":Number(v).toFixed(d==null?0:d);}',
' function api(n,p,cb){apex.server.process(n,p,{dataType:"json",success:cb,error:function(){$("swErr").style.display="block";$("swErr").textContent="El servidor respondio con error; revisa el log de la base.";$("swBtn").disabled=false;$("swSpin").styl'
||'e.display="none";}});}',
' function fmtDif(n){var x=Math.round(Number(n)||0);return x>0?"+"+x.toLocaleString("es-ES"):x<0?x.toLocaleString("es-ES"):"0";}',
' function pintaDif(id,n){var el=$(id+"V");var x=Math.round(Number(n)||0);el.textContent=fmtDif(x);el.className="difval"+(x>0?" pos":x<0?" neg":" zero");}',
' function ponSlider(id,min,max){var el=$(id);var v=Math.round(Number(el.value)||0);min=Math.round(min);max=Math.round(max);if(min>max){var m=min;min=max;max=m;}el.min=min;el.max=max;el.step=1;el.value=Math.min(Math.max(v,min),max);pintaDif(id,el.valu'
||'e);}',
' function actualizarLimites(r){',
'  var d={pop:Number($("swPop").value)||0,viv:Number($("swViv").value)||0,sal:Number($("swSal").value)||0,esc:Number($("swEsc").value)||0,par:Number($("swPar").value)||0};',
'  var base={pop:Math.max(0,Number(r.poblacion_base_anio)||0),viv:Math.max(0,(Number(r.viviendas_despues)||0)-d.viv),sal:Math.max(0,(Number(r.centros_salud_despues)||0)-d.sal),esc:Math.max(0,(Number(r.escuelas_despues)||0)-d.esc),par:Math.max(0,(Numbe'
||'r(r.paradas_despues)||0)-d.par)};',
'  ponSlider("swPop",-base.pop,3*base.pop);',
'  ["swViv","swSal","swEsc","swPar"].forEach(function(id){var b=base[id.slice(2).toLowerCase()];ponSlider(id,-b,Math.max(3*b,20));});',
' }',
' function colMej(a,b){var x=Number(b)-Number(a);return x>0?"#0f766e":x<0?"#b91c1c":"#64748b";}',
' function fila(t,a,b,dec,col){return "<tr><td>"+t+"</td><td class=\"num\">"+num(a,dec)+"</td><td class=\"num\""+(col?" style=\"color:"+col+"\"":"")+">"+num(b,dec)+"</td></tr>";}',
' function render(r){',
'  if(!r||typeof r!=="object"||!("indice_despues" in r)){$("swErr").style.display="block";$("swErr").textContent="El JSON no parece una respuesta del simulador.";return;}',
'  RESULT=r;$("swBtnDl").disabled=false;',
'  $("swStage").classList.remove("locked");$("swOverlay").style.display="none";',
'  $("swIdxA").textContent=num(r.indice_antes,1);$("swIdxB").textContent=num(r.indice_despues,1);',
'  var d=num(r.delta_indice,1);var deltaN=Number(r.delta_indice);$("swDelta").textContent=(deltaN>0?"+ ":"")+d+(deltaN>0?" (mejora)":deltaN<0?" (caida)":"");',
'   $("swDelta").style.color=deltaN>=0?"#0f766e":"#b91c1c";',
'   $("swIdxB").style.color=deltaN>0?"#0f766e":deltaN<0?"#b91c1c":"";',
'  $("swLimit").textContent="factor limitante: "+esc(r.factor_limitante);',
'  $("swPobBase").textContent=num(r.poblacion_base_anio,0);',
'  $("swBand").textContent=num(r.poblacion_anio_p10,0)+" - "+num(r.poblacion_anio_p90,0);',
'  $("swFactor").textContent="x"+num(r.factor_m3,4);',
'  $("swPob").textContent=num(r.poblacion_despues,0);',
'  $("swPobS").textContent=num(r.poblacion_antes,0)+" -> "+num(r.poblacion_despues,0)+" hab.";',
'  var dims=[["Demografia","dem"],["Vivienda","viv"],["Servicios","ser"],["Accesibilidad","acc"],["Empleo","emp"]];',
'  $("swDims").innerHTML=dims.map(function(x){var a=r["dim_"+x[1]+"_antes"],b=r["dim_"+x[1]+"_despues"];',
'   var col=colMej(a,b);',
'   return "<div class=\"dim\"><span>"+x[0]+"</span><span class=\"track\"><i class=\"before\" style=\"width:"+num(a)+"%\"></i></span><span class=\"track\"><i class=\"after\" style=\"width:"+num(b)+"%;background:"+col+"\"></i></span><b>"+num(a,1)+" <sp'
||'an style=\"color:"+col+"\">&rarr; "+num(b,1)+"</span></b></div>";',
'  }).join("");',
'  $("swRatios").innerHTML="<thead><tr><th>Ratio</th><th class=\"num\">Antes</th><th class=\"num\">Escenario</th></tr></thead><tbody>"',
'   +fila("Centros de salud por 10.000 hab.",r.salud_10k_antes,r.salud_10k_despues,2,colMej(r.salud_10k_antes,r.salud_10k_despues))',
'   +fila("Escuelas por 1.000 hab.",r.escuelas_1000_antes,r.escuelas_1000_despues,3,colMej(r.escuelas_1000_antes,r.escuelas_1000_despues))',
'   +fila("Paradas por 1.000 hab.",r.paradas_1000_antes,r.paradas_1000_despues,3,colMej(r.paradas_1000_antes,r.paradas_1000_despues))',
'   +fila("Viviendas por 1.000 hab.",r.viv_1000_antes,r.viv_1000_despues,1,colMej(r.viv_1000_antes,r.viv_1000_despues))',
'   +"</tbody>";',
'  $("swChoques").innerHTML="<thead><tr><th>Recurso</th><th class=\"num\">Antes</th><th class=\"num\">Escenario</th></tr></thead><tbody>"',
'   +fila("Poblacion",r.poblacion_antes,r.poblacion_despues,0)',
'   +fila("Viviendas",r.viviendas_antes,r.viviendas_despues,0)',
'   +fila("Centros de salud",r.centros_salud_antes,r.centros_salud_despues,0)',
'   +fila("Escuelas",r.escuelas_antes,r.escuelas_despues,0)',
'   +fila("Paradas",r.paradas_antes,r.paradas_despues,0)',
'   +"</tbody>";',
'  actualizarLimites(r);',
' }',
' function run(){',
'  if($("swBtn").disabled)return;',
'  $("swErr").style.display="none";',
'  $("swBtn").disabled=true;$("swSpin").style.display="block";',
'  api("SIMULAR",{x01:$("swCod").value,x02:$("swAnio").value,x03:$("swPop").value||0,x04:$("swViv").value||0,x05:$("swSal").value||0,x06:$("swEsc").value||0,x07:$("swPar").value||0},function(r){',
'   $("swBtn").disabled=false;$("swSpin").style.display="none";',
'   render(r);',
'   if(!BASE){',
'    BASE=true;',
'    ["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).disabled=false;});',
'    $("swBtn").textContent="Reejecutar Simulaci\u00f3n";',
'   }',
'  });',
' }',
' function aCsv(o){',
'  var ks=Object.keys(o),lin=[ks.join(";")];',
'  lin.push(ks.map(function(k){var v=o[k];if(v==null)return "";v=""+v;return (v.indexOf(";")>=0||v.indexOf("\"")>=0||v.indexOf("\n")>=0)?"\""+v.replace(/"/g,"\"\"")+"\"":v;}).join(";"));',
'  return "\uFEFF"+lin.join("\n");',
' }',
' function descargar(fmt){',
'  if(!RESULT)return;',
'  var nom="simulador-"+(RESULT.cod||"escenario")+"-"+(RESULT.anio_simulado||"");',
'  var blob,ext;',
'  if(fmt==="csv"){blob=new Blob([aCsv(RESULT)],{type:"text/csv;charset=utf-8"});ext="csv";}',
'  else{blob=new Blob([JSON.stringify(RESULT,null,1)],{type:"application/json"});ext="json";}',
'  var u=URL.createObjectURL(blob);',
'  var a=document.createElement("a");',
'  a.href=u;a.download=nom+"."+ext;',
'  document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);',
' }',
' $("swFile").addEventListener("change",function(){',
'  var f=this.files&&this.files[0];if(!f)return;',
'  var rd=new FileReader();',
'  rd.onload=function(){',
'   try{var r=JSON.parse(rd.result);$("swErr").style.display="none";render(r);',
'    if(!BASE){BASE=true;["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).disabled=false;});$("swBtn").textContent="Reejecutar Simulaci\u00f3n";}',
'   }',
'   catch(e){$("swErr").style.display="block";$("swErr").textContent="El fichero no es un JSON valido.";}',
'  };',
'  rd.readAsText(f);this.value="";',
' });',
' function boot(){',
'  var o="",y;for(y=2025;y<=2035;y++){o+="<option value=\""+y+"\">"+y+"</option>";}',
'  $("swAnio").innerHTML=o;$("swAnio").value="2030";',
'  api("DATOS",{},function(rows){',
'   var m=rows||[];',
'   $("swCod").innerHTML=m.map(function(x){return "<option value=\""+esc(x.cod)+"\">"+esc(x.nombre)+"</option>";}).join("");',
'  });',
'  ["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).addEventListener("input",function(){pintaDif(id,this.value);});});',
'  $("swBtnDl").addEventListener("click",function(ev){ev.stopPropagation();var m=$("swDlMenu");m.style.display=(m.style.display==="block")?"none":"block";});',
'  document.querySelectorAll("#swDlMenu button").forEach(function(b){b.addEventListener("click",function(ev){ev.stopPropagation();descargar(b.getAttribute("data-fmt"));$("swDlMenu").style.display="none";});});',
'  document.addEventListener("click",function(){$("swDlMenu").style.display="none";});',
'  $("swBtnImp").addEventListener("click",function(){$("swFile").click();});',
'  $("swBtn").addEventListener("click",run);',
'  document.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); run(); } });',
' }',
' (function w(){ if(window.apex&&window.apex.server){setTimeout(boot,400);} else {setTimeout(w,100);} })();',
'})();',
'</script>',
'</script>~'');',
'END;'))
,p_plug_source_type=>'NATIVE_PLSQL'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(8900550584000011)
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
 p_id=>wwv_flow_imp.id(8900550584000012)
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
 p_id=>wwv_flow_imp.id(8900550584000016)
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
 p_id=>wwv_flow_imp.id(8900550584000015)
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
 p_id=>wwv_flow_imp.id(8900550584000019)
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
 p_id=>wwv_flow_imp.id(8900550584000018)
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
prompt --application/deployment/definition
begin
wwv_flow_imp.g_varchar2_table := wwv_flow_imp.empty_varchar2_table;
wwv_flow_imp_shared.create_install(
 p_id=>wwv_flow_imp.id(10237754273234617)
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
