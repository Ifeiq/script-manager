try:    import flet as ft
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
    import flet as ft

def back(page: ft.Page, page_old):
    clear_screen(page)
    page.add(*page_old)

def clear_screen(page: ft.Page):
    page.controls.clear()
    page.update()

def connect_adb_wifi(page: ft.Page, page_old):
    import subprocess
    import os
    
    # Caminho para o platform-tools (ajuste conforme necessário)
    platform_tools_path = r"./platform-tools/"
    adb_path = os.path.join(platform_tools_path, "adb.exe")
    
    # Obter o IP do campo de texto
    ip_field = None
    for control in page.controls:
        if hasattr(control, 'content') and hasattr(control.content, 'label'):
            if control.content.label == "Digite o IP do dispositivo":
                ip_field = control.content
                break
    
    if ip_field and ip_field.value:
        ip = ip_field.value.strip()
        
        try:
            result = subprocess.run(
                [adb_path, "connect", ip], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                clear_screen(page)
                page.add(
                    ft.Container(
                        content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
                        alignment=ft.alignment.top_left,
                    ),
                    ft.Container(
                        content=ft.Text("Conexão ADB estabelecida!", color="green", size=20, weight="bold"),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text(f"Dispositivo conectado: {ip}", color="blue", size=16),
                        alignment=ft.alignment.center,
                    ),
                )
            else:
                clear_screen(page)
                page.add(
                    ft.Container(
                        content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
                        alignment=ft.alignment.top_left,
                    ),
                    ft.Container(
                        content=ft.Text("Erro na conexão ADB", color="red", size=20, weight="bold"),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text(f"Erro: {result.stderr}", color="red", size=14),
                        alignment=ft.alignment.center,
                    ),
                )
        except subprocess.TimeoutExpired:
            clear_screen(page)
            page.add(
                ft.Container(
                    content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
                    alignment=ft.alignment.top_left,
                ),
                ft.Container(
                    content=ft.Text("Timeout na conexão", color="red", size=20, weight="bold"),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text("O dispositivo pode estar offline ou o IP está incorreto", color="red", size=14),
                    alignment=ft.alignment.center,
                ),
            )
        except FileNotFoundError:
            clear_screen(page)
            page.add(
                ft.Container(
                    content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
                    alignment=ft.alignment.top_left,
                ),
                ft.Container(
                    content=ft.Text("ADB não encontrado", color="red", size=20, weight="bold"),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text(f"Verifique se o platform-tools está em: {platform_tools_path}", color="red", size=12),
                    alignment=ft.alignment.center,
                ),
            )
    else:
        # Campo vazio
        clear_screen(page)
        page.add(
            ft.Container(
                content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
                alignment=ft.alignment.top_left,
            ),
            ft.Container(
                content=ft.Text("Digite um IP válido", color="red", size=20, weight="bold"),
                alignment=ft.alignment.center,
            ),
        )

def WIFI(page: ft.Page, page_old):
    # Widgets da página de conexão para voltar
    connect_widgets = [
        ft.Container(
            content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
            alignment=ft.alignment.top_left,
        ),
        ft.Container(
            content=ft.Text("Escolha uma opção de conexão", color="blue", size=20, weight="bold"),
            alignment=ft.alignment.center,
        ),
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.ElevatedButton(text="Conectar por Wi-fi", color="blue", on_click=lambda e: WIFI(page, page_old)),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(text="Conectar por Cabo", color="blue", on_click=lambda e: connect(page, page_old)),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.alignment.center,
        ),
    ]
    
    clear_screen(page)
    page.add(
        ft.Container(
            content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, connect_widgets)),
            alignment=ft.alignment.top_left,
        ),
        ft.Container(
            content=ft.Text("Conecte por Wi-fi", color="blue", size=20, weight="bold"),
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=ft.TextField(
                label="Digite o IP do dispositivo",
                hint_text="Exemplo: 192.168.1.100",
                width=300,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=ft.ElevatedButton(
                text="Conectar via ADB", 
                color="green",
                on_click=lambda e: connect_adb_wifi(page, connect_widgets)
            ),
            alignment=ft.alignment.center,
        ),
    )

def connect(page: ft.Page, page_old):
    clear_screen(page)
    page.add(
        ft.Container(
            content=ft.ElevatedButton(text="Voltar", color="blue", on_click=lambda e: back(page, page_old)),
            alignment=ft.alignment.top_left,
        ),
        ft.Container(
            content=ft.Text("Escolha uma opção de conexão", color="blue", size=20, weight="bold"),
            alignment=ft.alignment.center,
        ),

        ft.Column(
            controls=[
                ft.Container(
                    content=ft.ElevatedButton(text="Conectar por Wi-fi", color="blue", on_click=lambda e: WIFI(page, page_old)),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(text="Conectar por Cabo", color="blue", on_click=lambda e: connect(page, page_old)),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.alignment.center,
        ),
    )
    

def main(page: ft.Page):
    main_widgets = [
        ft.Container(
            content=ft.Text("Script Manager", color="blue", size=20, weight="bold"),
            alignment=ft.alignment.center,
        ),

        ft.Column(
            controls=[
                ft.Container(
                    content=ft.ElevatedButton(text="Conectar em um dispositivo", color="blue", on_click=lambda e: connect(page, main_widgets)),
                    alignment=ft.alignment.center,
                ),
                
            ],
            alignment=ft.alignment.center,
        ),
    ]
    
    page.add(*main_widgets)

ft.app(target=main)