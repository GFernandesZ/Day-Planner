interface TaskItem {
  id: number;
  owner: number; // PK do owner
  name: string; // Nome da categoria da tarefa
  priority: 'low' | 'medium' | 'high' | 'urgent'; // Prioridade da categoria
  items_list_display: string[]; // Lista de strings dos itens
  // Se 'itemX_text' são campos diretos no modelo, o serializer pode retorná-los diretamente
  // item1_text?: string;
  // item2_text?: string; // e assim por diante
}

interface NoteItem {
  id: number;
  owner: number;
  title: string;
  topic: string;
  content: string;
  border_color: string; // Ex: 'border-primary'
  foto?: string; // O caminho do arquivo de foto, como salvo no banco
  foto_url: string | null; // A URL completa para exibir a foto
  created_at: string; // Data string ISO
}

interface DateItem {
  id: number;
  owner: number;
  title: string;
  date: string; // Data string ISO
  description: string;
  type: 'comemorativa' | 'importante';
  category: string;
  color: string; // Ex: 'success', 'danger'
  is_fixed: boolean;
  created_at: string;
}

// Mapeamento de cores para meses (copiado do Django models.py)
const MONTH_COLORS: { [key: number]: string } = {
  1: 'badge-january',
  2: 'badge-february',
  3: 'badge-march',
  4: 'badge-april',
  5: 'badge-may',
  6: 'badge-june',
  7: 'badge-july',
  8: 'badge-august',
  9: 'badge-september',
  10: 'badge-october',
  11: 'badge-november',
  12: 'badge-december',
};

// Frases do Dia (copiado do Django views.py)
const DAILY_QUOTES = [
  "O sucesso é a soma de pequenos esforços repetidos todos os dias.",
  "Acredite em si mesmo e tudo será possível.",
  "A persistência é o caminho do êxito.",
  "Grandes conquistas exigem grandes sacrifícios.",
  "Faça hoje o que ninguém faz, e amanhã terá o que ninguém tem.",
  "A mente é tudo. O que você pensa, você se torna.",
  "Não espere por oportunidades, crie-as.",
  "O futuro pertence àqueles que acreditam na beleza de seus sonhos.",
  "Seja a mudança que você deseja ver no mundo.",
  "A vida é 10% o que acontece com você e 90% como você reage a isso.",
  "O único lugar onde o sucesso vem antes do trabalho é no dicionário.",
  "A felicidade não é algo pronto. Ela vem de suas próprias ações.",
  "Comece onde você está. Use o que você tem. Faça o que você pode.",
  "Não importa o quão devagar você vá, desde que não pare.",
  "Nós nos tornamos o que pensamos na maior parte do tempo.",
  "A adversidade revela gênios, a prosperidade os esconde.",
  "Sonhe grande e ouse falhar.",
  "Aja como se o que você faz fizesse a diferença. Faz.",
  "Não se preocupe com falhas; preocupe-se com as chances que você perde quando não tenta.",
  "A melhor vingança é um sucesso massivo.",
  "O segredo de ir em frente é começar.",
  "A vida é uma escalada, mas a vista é ótima.",
  "Sua limitação - é apenas sua imaginação.",
  "O sucesso é a soma de pequenos erros bem corrigidos.",
  "Seja a luz no fim do túnel.",
  "Faça do hoje um dia incrível.",
  "Cada dia é uma nova oportunidade.",
  "Aprenda com o ontem, viva o hoje, tenha esperança para o amanhã.",
  "A vida é uma jornada, não um destino.",
  "O poder está em você. Acredite!",
  "Inspire, persista, conquiste."
];
