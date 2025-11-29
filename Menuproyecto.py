from utiles import inicializar_base_datos, mostrar_menu, titulo

if __name__ == "__main__":
    inicializar_base_datos()
    titulo("Bienvenido/a al sistema de gestion básica de producto")
    titulo("Por favor elija una de las opciones para continuar")
    mostrar_menu() # Ejecutar menú
