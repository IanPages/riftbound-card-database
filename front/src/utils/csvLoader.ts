import Papa from 'papaparse';

export interface Card {
  id: string; // Generating a unique ID from name+set
  name: string;
  set: string;
  quantity: number;
  type: string;
  color: string;
  altArt: boolean;
  overnumbered: boolean;
  image: string;
}

/**
 * Fetches and parses a CSV file from the public directory.
 * @param csvPath Path to the CSV file (e.g., "/cards.csv" or "/all_cards_database.csv")
 */
export const loadCardsFromCSV = async (csvPath: string = '/cards.csv'): Promise<Card[]> => {
  try {
    const response = await fetch(csvPath);
    if (!response.ok) {
      throw new Error(`Failed to fetch CSV: ${response.statusText}`);
    }
    const csvText = await response.text();

    return new Promise((resolve, reject) => {
      Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          const parsedCards = results.data.map((row: any, index: number) => ({
            id: `${row.set}-${row.name}-${index}`, // Ensure unique key for React
            name: row.name || 'Unknown',
            set: row.set || '???',
            quantity: parseInt(row.quantity, 10) || 1,
            type: row.type ? row.type.toUpperCase() : 'UNKNOWN',
            color: row.color || 'NONE',
            altArt: row.altArt === 'true',
            overnumbered: row.overnumbered === 'true',
            image: row.image || '',
          }));
          resolve(parsedCards as Card[]);
        },
        error: (error: any) => {
          reject(error);
        }
      });
    });
  } catch (error) {
    console.error("Error loading cards:", error);
    return [];
  }
};
