to#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <stdexcept>

class AFD {
private:
    // Q: conjunto de estados
    std::unordered_set<std::string> estados;

    // Σ: alfabeto
    std::unordered_set<char> alfabeto;

    // δ: função de transição
    std::unordered_map<
        std::string,
        std::unordered_map<char, std::string>
    > transicoes;

    // q₀: estado inicial
    std::string estadoInicial;

    // F: conjunto de estados finais
    std::unordered_set<std::string> estadosFinais;

public:

    void adicionarEstado(const std::string& estado) {
        estados.insert(estado);
    }

    void adicionarSimbolo(char simbolo) {
        alfabeto.insert(simbolo);
    }

    void definirEstadoInicial(const std::string& estado) {
        if (!estados.contains(estado)) {
            throw std::invalid_argument(
                "O estado inicial deve pertencer a Q."
            );
        }

        estadoInicial = estado;
    }

    void adicionarEstadoFinal(const std::string& estado) {
        if (!estados.contains(estado)) {
            throw std::invalid_argument(
                "O estado final deve pertencer a Q."
            );
        }

        estadosFinais.insert(estado);
    }

    void adicionarTransicao(
        const std::string& estado,
        char simbolo,
        const std::string& proximoEstado
    ) {
        if (!estados.contains(estado)) {
            throw std::invalid_argument(
                "Estado de origem inexistente."
            );
        }

        if (!estados.contains(proximoEstado)) {
            throw std::invalid_argument(
                "Estado de destino inexistente."
            );
        }

        if (!alfabeto.contains(simbolo)) {
            throw std::invalid_argument(
                "Simbolo inexistente no alfabeto."
            );
        }

        transicoes[estado][simbolo] = proximoEstado;
    }

    bool aceita(const std::string& palavra) const {

        std::string estado = estadoInicial;

        for (char simbolo : palavra) {

            // Verifica se o símbolo pertence a Σ.
            if (!alfabeto.contains(simbolo)) {
                return false;
            }

            // Procura δ(estado, símbolo).
            auto estadoIt = transicoes.find(estado);

            if (estadoIt == transicoes.end()) {
                return false;
            }

            auto simboloIt = estadoIt->second.find(simbolo);

            if (simboloIt == estadoIt->second.end()) {
                return false;
            }

            // q ← δ(q, símbolo)
            estado = simboloIt->second;
        }

        // w é aceita se q ∈ F.
        return estadosFinais.contains(estado);
    }
};


/*
 * Lê o conteúdo de fonte.lin.
 */
std::string lerArquivo(const std::string& nomeArquivo) {

    std::ifstream arquivo(nomeArquivo);

    if (!arquivo.is_open()) {
        throw std::runtime_error(
            "Nao foi possivel abrir o arquivo: " + nomeArquivo
        );
    }

    // Lê todo o arquivo, inclusive espaços e quebras de linha.
    std::string conteudo(
        (std::istreambuf_iterator<char>(arquivo)),
        std::istreambuf_iterator<char>()
    );

    return conteudo;
}


int main() {

    try {

        // ==================================================
        // CONSTRUÇÃO DO AFD
        // ==================================================

        AFD afd;

        // Q
        afd.adicionarEstado("q0");
        afd.adicionarEstado("q1");
        afd.adicionarEstado("q2");

        // Σ
        afd.adicionarSimbolo('0');
        afd.adicionarSimbolo('1');

        // q₀
        afd.definirEstadoInicial("q0");

        // F
        afd.adicionarEstadoFinal("q2");

        // δ
        afd.adicionarTransicao("q0", '0', "q1");
        afd.adicionarTransicao("q0", '1', "q0");

        afd.adicionarTransicao("q1", '0', "q1");
        afd.adicionarTransicao("q1", '1', "q2");

        afd.adicionarTransicao("q2", '0', "q1");
        afd.adicionarTransicao("q2", '1', "q0");


        // ==================================================
        // LEITURA DO ARQUIVO
        // ==================================================

        const std::string nomeArquivo = "fonte.lin";

        std::string palavra = lerArquivo(nomeArquivo);


        // ==================================================
        // EXECUÇÃO DO AFD
        // ==================================================

        if (afd.aceita(palavra)) {
            std::cout << "ACEITA\n";
        }
        else {
            std::cout << "REJEITADA\n";
        }

    }
    catch (const std::exception& erro) {

        std::cerr << "Erro: "
                  << erro.what()
                  << '\n';

        return 1;
    }

    return 0;
}