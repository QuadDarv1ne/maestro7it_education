import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';

// Моковые данные для демонстрации
const SAMPLE_DATABASES = [
  {
    id: 'chinook',
    name: 'Chinook Music Store',
    tables: ['Artist', 'Album', 'Track', 'Customer', 'Invoice'],
    description: 'Музыкальный магазин'
  },
  {
    id: 'northwind',
    name: 'Northwind Business',
    tables: ['Products', 'Categories', 'Customers', 'Orders'],
    description: 'Бизнес-аналитика'
  }
];

const SAMPLE_QUERIES = [
  {
    id: 1,
    database: 'chinook',
    query: 'SELECT Name FROM Artist LIMIT 5;',
    description: 'Показать 5 исполнителей'
  },
  {
    id: 2,
    database: 'northwind',
    query: 'SELECT ProductName, UnitPrice FROM Products ORDER BY UnitPrice DESC LIMIT 5;',
    description: '5 самых дорогих продуктов'
  }
];

export default function App() {
  const [currentDatabase, setCurrentDatabase] = useState('chinook');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isExecuting, setIsExecuting] = useState(false);

  const executeQuery = () => {
    if (!query.trim()) {
      Alert.alert('Ошибка', 'Введите SQL-запрос');
      return;
    }

    setIsExecuting(true);
    
    // Симуляция выполнения запроса
    setTimeout(() => {
      try {
        // Здесь будет реальное выполнение SQL
        const mockResults = [
          { column1: 'Результат 1', column2: 'Данные 1' },
          { column1: 'Результат 2', column2: 'Данные 2' },
          { column1: 'Результат 3', column2: 'Данные 3' }
        ];
        
        setResults(mockResults);
        Alert.alert('Успех', `Запрос выполнен. Найдено ${mockResults.length} записей.`);
      } catch (error) {
        Alert.alert('Ошибка', 'Неверный SQL-запрос');
      } finally {
        setIsExecuting(false);
      }
    }, 1000);
  };

  const loadSampleQuery = (sampleQuery) => {
    setQuery(sampleQuery.query);
    setCurrentDatabase(sampleQuery.database);
  };

  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      
      <Text style={styles.title}>SQL Learning App</Text>
      
      {/* Выбор базы данных */}
      <View style={styles.databaseSelector}>
        <Text style={styles.sectionTitle}>База данных:</Text>
        <ScrollView horizontal style={styles.databaseList}>
          {SAMPLE_DATABASES.map(db => (
            <TouchableOpacity
              key={db.id}
              style={[
                styles.databaseButton,
                currentDatabase === db.id && styles.activeDatabaseButton
              ]}
              onPress={() => setCurrentDatabase(db.id)}
            >
              <Text style={[
                styles.databaseButtonText,
                currentDatabase === db.id && styles.activeDatabaseButtonText
              ]}>
                {db.name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Редактор SQL */}
      <View style={styles.querySection}>
        <Text style={styles.sectionTitle}>SQL Запрос:</Text>
        <TextInput
          style={styles.queryInput}
          multiline
          numberOfLines={4}
          placeholder="Введите ваш SQL-запрос здесь..."
          value={query}
          onChangeText={setQuery}
        />
        
        <TouchableOpacity
          style={[styles.executeButton, isExecuting && styles.disabledButton]}
          onPress={executeQuery}
          disabled={isExecuting}
        >
          <Text style={styles.executeButtonText}>
            {isExecuting ? 'Выполняется...' : 'Выполнить'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Примеры запросов */}
      <View style={styles.samplesSection}>
        <Text style={styles.sectionTitle}>Примеры запросов:</Text>
        <ScrollView style={styles.samplesList}>
          {SAMPLE_QUERIES.filter(sq => sq.database === currentDatabase).map(sample => (
            <TouchableOpacity
              key={sample.id}
              style={styles.sampleItem}
              onPress={() => loadSampleQuery(sample)}
            >
              <Text style={styles.sampleDescription}>{sample.description}</Text>
              <Text style={styles.sampleQuery} numberOfLines={2}>
                {sample.query}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Результаты */}
      {results.length > 0 && (
        <View style={styles.resultsSection}>
          <Text style={styles.sectionTitle}>Результаты ({results.length} записей):</Text>
          <ScrollView style={styles.resultsList}>
            {results.map((row, index) => (
              <View key={index} style={styles.resultRow}>
                <Text>{JSON.stringify(row)}</Text>
              </View>
            ))}
          </ScrollView>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
    paddingTop: 50,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 10,
    color: '#555',
  },
  databaseSelector: {
    marginBottom: 20,
  },
  databaseList: {
    flexDirection: 'row',
  },
  databaseButton: {
    backgroundColor: '#e0e0e0',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 20,
    marginRight: 10,
  },
  activeDatabaseButton: {
    backgroundColor: '#007AFF',
  },
  databaseButtonText: {
    color: '#666',
    fontWeight: '500',
  },
  activeDatabaseButtonText: {
    color: 'white',
  },
  querySection: {
    marginBottom: 20,
  },
  queryInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    backgroundColor: 'white',
    fontSize: 16,
    minHeight: 100,
    marginBottom: 15,
    textAlignVertical: 'top',
  },
  executeButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  disabledButton: {
    backgroundColor: '#ccc',
  },
  executeButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  samplesSection: {
    marginBottom: 20,
    flex: 1,
  },
  samplesList: {
    flex: 1,
  },
  sampleItem: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#eee',
  },
  sampleDescription: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 5,
    color: '#333',
  },
  sampleQuery: {
    fontSize: 14,
    color: '#666',
    fontFamily: 'monospace',
  },
  resultsSection: {
    flex: 1,
  },
  resultsList: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#eee',
  },
  resultRow: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
});