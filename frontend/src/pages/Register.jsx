import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import IluminatiLogo from '../components/IluminatiLogo';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const { register } = useAuth();
  const navigate = useNavigate();

  const calculatePasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/\d/)) strength++;
    if (password.match(/[^a-zA-Z\d]/)) strength++;
    return strength;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (name === 'password') {
      setPasswordStrength(calculatePasswordStrength(value));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validácia
    if (formData.password !== formData.confirmPassword) {
      setError('Heslá sa nezhodujú');
      return;
    }

    if (formData.password.length < 8) {
      setError('Heslo musí mať aspoň 8 znakov');
      return;
    }

    if (passwordStrength < 2) {
      setError('Heslo je príliš slabé. Použite veľké, malé písmená a čísla.');
      return;
    }

    setLoading(true);

    const result = await register(formData.email, formData.password, formData.fullName);

    if (result.success) {
      // Presmerovať na login po úspešnej registrácii
      navigate('/login', { state: { message: 'Registration successful! Please sign in.' } });
    } else {
      setError(result.error || 'Registration failed');
    }

    setLoading(false);
  };

  const getStrengthColor = () => {
    if (passwordStrength <= 1) return 'bg-red-500';
    if (passwordStrength === 2) return 'bg-yellow-500';
    if (passwordStrength === 3) return 'bg-blue-500';
    return 'bg-green-500';
  };

  const getStrengthText = () => {
    if (passwordStrength <= 1) return 'Slabé';
    if (passwordStrength === 2) return 'Priemerné';
    if (passwordStrength === 3) return 'Dobré';
    return 'Silné';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
        <div className="text-center mb-8">
          <IluminatiLogo className="mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-white mb-2">Vytvoriť účet</h1>
          <p className="text-blue-200">Pripojte sa k ILUMINATI SYSTEM už dnes</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-500/20 border border-red-500 text-red-100 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="fullName" className="block text-sm font-medium text-white mb-2">
              Celé meno
            </label>
            <input
              id="fullName"
              name="fullName"
              type="text"
              value={formData.fullName}
              onChange={handleChange}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ján Novák"
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-white mb-2">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="vas@email.sk"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-white mb-2">
              Heslo
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="••••••••"
            />
            {formData.password && (
              <div className="mt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-blue-200">Sila hesla:</span>
                  <span className={`text-xs font-semibold ${getStrengthColor().replace('bg-', 'text-')}`}>
                    {getStrengthText()}
                  </span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${getStrengthColor()}`}
                    style={{ width: `${(passwordStrength / 4) * 100}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-white mb-2">
              Potvrdenie hesla
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="••••••••"
            />
            {formData.confirmPassword && formData.password !== formData.confirmPassword && (
              <p className="mt-1 text-xs text-red-300">Heslá sa nezhodujú</p>
            )}
          </div>

          <div className="flex items-center">
            <input
              id="terms"
              type="checkbox"
              required
              className="rounded border-white/20 text-blue-600 focus:ring-blue-500"
            />
            <label htmlFor="terms" className="ml-2 text-sm text-blue-200">
              Súhlasím s{' '}
              <Link to="/vop" className="text-blue-300 hover:text-blue-200 underline">
                Všeobecnými obchodnými podmienkami (VOP)
              </Link>{' '}
              a{' '}
              <Link to="/privacy" className="text-blue-300 hover:text-blue-200 underline">
                Zásadami ochrany osobných údajov
              </Link>
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Vytváranie účtu...' : 'Vytvoriť účet'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-blue-200">
            Už máte účet?{' '}
            <Link to="/login" className="text-blue-300 hover:text-blue-200 font-semibold">
              Prihlásiť sa
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;

