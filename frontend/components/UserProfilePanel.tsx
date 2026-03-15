'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Save, User, Sparkles, Trophy } from 'lucide-react'

interface UserProfile {
  name: string
  interests: string[]
  expertise_level: 'beginner' | 'intermediate' | 'advanced'
  learning_goal: string
}

interface UserProfilePanelProps {
  onSave?: (profile: UserProfile) => Promise<void>
}

const PREDEFINED_INTERESTS = [
  'LLMs',
  'AI Safety',
  'Practical Applications',
  'Open-Source AI',
  'Computer Vision',
  'NLP',
  'Robotics',
  'Multimodal AI',
  'Reasoning',
  'Fine-tuning',
  'Research Papers',
  'Industry News'
]

const DEFAULT_PROFILE: UserProfile = {
  name: 'User',
  interests: ['LLMs', 'AI Safety', 'Practical Applications', 'Open-Source AI'],
  expertise_level: 'intermediate',
  learning_goal: 'Master AI developments daily'
}

export default function UserProfilePanel({ onSave }: UserProfilePanelProps) {
  const [profile, setProfile] = useState<UserProfile>(DEFAULT_PROFILE)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(false)

  const handleNameChange = (name: string) => {
    setProfile(prev => ({ ...prev, name }))
  }

  const handleInterestToggle = (interest: string) => {
    setProfile(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }))
  }

  const handleExpertiseChange = (level: UserProfile['expertise_level']) => {
    setProfile(prev => ({ ...prev, expertise_level: level }))
  }

  const handleGoalChange = (goal: string) => {
    setProfile(prev => ({ ...prev, learning_goal: goal }))
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      if (onSave) {
        await onSave(profile)
      }
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (error) {
      console.error('Failed to save profile:', error)
    } finally {
      setSaving(false)
    }
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <motion.div
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Success Message */}
      {success && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="p-4 bg-teal-500 bg-opacity-15 border border-teal-500 border-opacity-30 rounded-lg text-teal-400 flex items-center gap-2"
        >
          <Sparkles size={18} />
          Profile saved successfully!
        </motion.div>
      )}

      {/* Name Section */}
      <motion.div variants={itemVariants} className="glass rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <User className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-white">Your Name</h3>
        </div>
        <input
          type="text"
          value={profile.name}
          onChange={e => handleNameChange(e.target.value)}
          placeholder="Enter your name"
          className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors"
        />
        <p className="text-xs text-slate-400 mt-2">This will personalize your morning brief</p>
      </motion.div>

      {/* Expertise Level */}
      <motion.div variants={itemVariants} className="glass rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <Trophy className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-white">Expertise Level</h3>
        </div>
        <div className="space-y-3">
          {(['beginner', 'intermediate', 'advanced'] as const).map(level => (
            <label key={level} className="flex items-center gap-3 cursor-pointer group">
              <input
                type="radio"
                name="expertise"
                value={level}
                checked={profile.expertise_level === level}
                onChange={() => handleExpertiseChange(level)}
                className="w-4 h-4 accent-cyan-500 cursor-pointer"
              />
              <span className="text-slate-300 group-hover:text-white transition-colors capitalize font-medium">
                {level}
              </span>
              <span className="text-xs text-slate-400">
                {level === 'beginner' && 'Explain core concepts in simple terms'}
                {level === 'intermediate' && 'Balance depth with accessibility'}
                {level === 'advanced' && 'Deep technical details and research focus'}
              </span>
            </label>
          ))}
        </div>
      </motion.div>

      {/* Interests */}
      <motion.div variants={itemVariants} className="glass rounded-xl p-6 border border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-white">Your Interests</h3>
        </div>
        <p className="text-sm text-slate-400 mb-4">
          Select topics that matter to you. The brief will prioritize these areas.
        </p>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {PREDEFINED_INTERESTS.map(interest => (
            <motion.button
              key={interest}
              onClick={() => handleInterestToggle(interest)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`px-3 py-2 rounded-lg font-medium text-sm transition-all ${
                profile.interests.includes(interest)
                  ? 'bg-cyan-600 text-white border border-cyan-500'
                  : 'bg-slate-800 text-slate-300 border border-slate-600 hover:border-slate-500'
              }`}
            >
              {interest}
            </motion.button>
          ))}
        </div>
        <p className="text-xs text-slate-400 mt-4">
          Selected: {profile.interests.length > 0 ? profile.interests.join(', ') : 'None'}
        </p>
      </motion.div>

      {/* Learning Goal */}
      <motion.div variants={itemVariants} className="glass rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Learning Goal</h3>
        <textarea
          value={profile.learning_goal}
          onChange={e => handleGoalChange(e.target.value)}
          placeholder="e.g., Master the latest LLM developments and practical applications"
          rows={3}
          className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors resize-none"
        />
        <p className="text-xs text-slate-400 mt-2">
          This helps shape the tone and focus of your morning brief
        </p>
      </motion.div>

      {/* Save Button */}
      <motion.div
        variants={itemVariants}
        className="flex gap-3"
      >
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-colors"
        >
          <Save size={20} />
          {saving ? 'Saving...' : 'Save Profile'}
        </button>
      </motion.div>

      {/* Info Box */}
      <motion.div
        variants={itemVariants}
        className="p-4 bg-blue-500 bg-opacity-10 border border-blue-500 border-opacity-30 rounded-lg"
      >
        <p className="text-sm text-blue-200">
          <strong>ℹ️ Note:</strong> Your profile is used to personalize the morning brief. It filters content by your interests and adjusts technical depth based on your expertise level.
        </p>
      </motion.div>
    </motion.div>
  )
}
