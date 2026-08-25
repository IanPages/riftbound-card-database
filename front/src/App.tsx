import { useState, useEffect } from 'react';
import './App.css';
import { loadCardsFromCSV, type Card } from './utils/csvLoader';
import cardsCsvUrl from '../../riftbound/cards.csv?url';

const FILTERS = ['All', 'Legend', 'Unit', 'Rune', 'Spell', 'Gear', 'Battlefield', 'Token'];

function App() {
  const [cards, setCards] = useState<Card[]>([]);
  const [activeFilter, setActiveFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  // Load cards on component mount
  useEffect(() => {
    const fetchCards = async () => {
      const loadedCards = await loadCardsFromCSV(cardsCsvUrl);
      setCards(loadedCards);
      setLoading(false);
    };

    fetchCards();
  }, []);

  // Filter logic
  const filteredCards = cards.filter(card => {
    const matchesFilter = activeFilter === 'All' || card.type.toLowerCase() === activeFilter.toLowerCase();
    const matchesSearch = card.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      card.set.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="pb-5">
      {/* Hero Section */}
      <div className="container hero">
        <div className="row d-flex align-items-center justify-content-center pt-5">
          <div className="col-12">
            <h1 className="text-center share-tech-regular">Fokita nº1 Riftb DB</h1>
          </div>
        </div>
      </div>

      {/* Filters Section */}
      <div className="container">
        <div className="row d-flex align-items-center justify-content-center pt-3">
          <div className="btn-group flex-wrap filter-buttons" role="group">
            {FILTERS.map(filter => (
              <button
                key={filter}
                type="button"
                className={`btn btn-outline-primary filter-button ${activeFilter === filter ? 'active' : ''}`}
                onClick={() => setActiveFilter(filter)}
              >
                {filter}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Counter Section */}
      <div className="container text-center mt-3">
        <h6 className="share-tech-regular-v2">Total Cards: {filteredCards.length}</h6>
      </div>

      {/* Search Section */}
      <div className="container text-center">
        <input
          className="form-control w-75 mx-auto searchBar"
          type="search"
          placeholder="Search by card name or set number"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Card Grid */}
      <div className="container pt-5">
        <div className="row justify-content-center g-4">
          {loading ? (
            <div className="col-12 text-center mt-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <p className="mt-3 text-white">Loading cards...</p>
            </div>
          ) : filteredCards.length > 0 ? (
            filteredCards.map((card) => (
              <div className="col-6 col-md-4 col-lg-3 card-wrapper" key={card.id}>
                <div className="card-custom">
                  <img
                    src={card.image}
                    alt={card.name}
                    className="card-img"
                    loading="lazy"
                  />
                </div>
                <div className="card-caption">
                  {card.name} ({card.set})
                  <p>Quantity: {card.quantity} &nbsp; Type: {card.type} &nbsp; Color: {card.color}</p>
                </div>
              </div>
            ))
          ) : (
            <p className="text-center mt-4 text-white">No results found.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
