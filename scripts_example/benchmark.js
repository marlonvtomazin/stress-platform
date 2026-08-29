import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "1m", target: 10 }, // Ramp-up
    { duration: "2m", target: 20 }, // Carga constante
    { duration: "1m", target: 30 }, // Pico
    { duration: "1m", target: 0 },  // Ramp-down
  ],

  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.20"],
  },
};

const BASE_URL = "https://quickpizza.grafana.com";

export default function () {
  const chance = Math.random();

  let res;

  if (chance < 0.80) {
    // 80% sucesso
    res = http.get(`${BASE_URL}/`);
  } else if (chance < 0.90) {
    // 10% erro 404
    res = http.get(`${BASE_URL}/pagina-inexistente`);
  } else {
    // 10% erro 500
    res = http.get(`${BASE_URL}/api/status/500`);
  }

  check(res, {
    "status esperado": (r) => [200, 404, 500].includes(r.status),
  });

  // Tempo entre requisições (0,2 a 1,5 s)
  sleep(0.2 + Math.random() * 1.3);
}